""" persons API resource """

import datetime

from flask import request, g, current_app

from . import api, token_auth
from ..models import Person, Legacy
from ..decorators import json
from ..exceptions import CanNotAcceptPayment
from ...tasks.email import send_welcome_email


# === Resource CRUD ============================================================

@api.route('/persons/<int:id>', methods=['GET'])
@token_auth.login_required
@json
def get_person(id):  # pylint: disable=I0011,W0622
    """
    Returns single *person* with the given ``id``.

    .. sourcecode:: http

        GET /person/1 HTTP/1.1

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
            "_links": {
                "self": "/persons/1"
            },
            "avatar": null,
            "email": "jdoe@example.com",
            "first_name": "John",
            "id": 1,
            "last_name": "Doe",
            "status": "UNPAID"
        }


    :statuscode 200: person record included in the response body
    :statuscode 404: no person record with given ``id``
    """

    if current_app.config.get('IGNORE_AUTH') is not True:
        assert id == g.user.id, 'Access denied'  # pragma: no cover

    return Person.query.get_or_404(id)


@api.route('/persons/', methods=['POST'])
@json
def create_person():  # pylint: disable=I0011,W0622
    """
    Creates a new *person*.

    .. sourcecode:: http

        POST /person/ HTTP/1.1
        Content-Type: application/json

        {
            "first_name": "John",
            "last_name": "Doe",
            "email": "jdoe@example.com",
            "avatar": null,
        }

    .. sourcecode:: http

        HTTP/1.0 201 CREATED
        Content-Type: application/json
        Location: /persons/1

        {}


    :statuscode 201: new record created, url included in the `Location` header
    :statuscode 400: No/Incomplete/Bad value(s) given in the request body
    """

    p = Person()
    p.from_dict(request.json)
    p.save()

    if not current_app.config['TESTING']:
        try:
            send_welcome_email.delay(p.to_dict(), username=p.username)
        except:  # pylint: disable=I0011,W0702
            pass  # Ignore email errors

    return {}, 201, {'Location': p.url()}


@api.route('/persons/<int:id>', methods=['PUT'])
@token_auth.login_required
@json
def edit_person(id):  # pylint: disable=I0011,W0622
    """
    Modify existing *person* with the given ``id``.

    .. sourcecode:: http

        PUT /person/1 HTTP/1.1
        Content-Type: application/json

        {
            "first_name": "John",
            "last_name": "Smith"
        }

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json
        Location: /persons/1

        {}


    :statuscode 200: record modified
    :statuscode 400: No/Incomplete/Bad value(s) given in the request body
    :statuscode 404: no person record with given ``id``
    """

    if current_app.config.get('IGNORE_AUTH') is not True:
        assert id == g.user.id, 'Access denied'  # pragma: no cover

    p = Person.query.get_or_404(id)
    p.from_dict(request.json)
    p.save()

    return {}


# === Resource function ========================================================

@api.route('/persons/<int:id>/pay', methods=['PUT'])
@token_auth.login_required
@json
def accept_payment(id):  # pylint: disable=I0011,W0622
    """
    If the *person* with the given ``id`` already have an active legacy profile,
    it's lock_date will be extended (from this date) by number of
    LEGACY_EXTEND_DAYS (from app.config).

    If the person is not assigned a legacy profile, new one will be created and
    lock_date will be set to LEGACY_LOCK_DAYS from today.

    In either case the status of the legacy profile will be set to ACTIVE.

    Only persons in UNPAID or ACTIVE status can make payments.

    .. sourcecode:: http

        PUT /person/1/pay HTTP/1.1
        Content-Type: application/json

        {
        }

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        ... see /legacy/<id> ...


    :statuscode 200: person, legacy and payment information updated, legacy
                     record returned in the body
    :statuscode 404: no person record with given ``id``
    :statuscode 405: person in current status can't accept payment
    """

    if current_app.config.get('IGNORE_AUTH') is not True:
        assert id == g.user.id, 'Access denied'  # pragma: no cover

    p = Person.query.get_or_404(id)

    if p.status not in ['ACTIVE', 'UNPAID']:
        # Only Active or Unpaid persons can make payments
        raise CanNotAcceptPayment()

    #
    # TODO: Process payment using the information in request payload
    #

    # Get person's legacy
    l = p.legacy
    days = current_app.config.get('LEGACY_LOCK_DAYS', 30)

    # If person doesn't have a legacy, create new one
    if l is None or 1 > len(l):
        l = Legacy(owner=p)
        days = current_app.config.get('LEGACY_EXTEND_DAYS', 30)
    else:
        l = l[0]

    # Update legacy status to active
    l.status = 'ACTIVE'

    # Update legacy lock_date
    # When current lock date is in future:
    #   new_lock_date =  current_lock_date + days(from above)
    # When current lock date is past or missing:
    #   new_lock_date =  now + days(from above)
    if l.lock_date is None:
        l.lock_date = datetime.datetime.now()

    l.lock_date += datetime.timedelta(days=days)

    # Update person status to active
    p.status = 'ACTIVE'

    l.save()
    p.save()

    return l
