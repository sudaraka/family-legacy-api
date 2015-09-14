""" event API resource """

from flask import g, current_app, request

from sqlalchemy.exc import IntegrityError

from .... import db
from ... import api, token_auth
from ....models import Legacy, Event
from ....decorators import json
from ....exceptions import IncompleteData, Http403

# === Resource CRUD ============================================================


@api.route('/legacy/<int:legacy_id>/events', methods=['GET'])
@token_auth.login_required
@json
def get_events(legacy_id):  # pylint: disable=I0011,W0622
    """
    Returns all *events* assigned to *legacy* with the given ``id``.

    .. sourcecode:: http

        GET /legacy/1/events HTTP/1.1

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
            "events": [
                {
                    "_links": {
                        "self": "http://127.0.0.1:5000/legacy/1/events/1"
                    },
                    "day": 12,
                    "month": 1,
                    "name": "Test event 1",
                    "status": "ENABLED"
                },
                ...
            ]
        }


    :statuscode 200: event records included in the response body
    :statuscode 404: no legacy record with given ``id``
    """

    l = Legacy.query.get_or_404(legacy_id)

    if current_app.config.get('IGNORE_AUTH') is not True:  # pragma: no cover
        if not l.can_view(g.user.id):
            raise Http403('Access denied')

    return {"events": [e.to_dict(True) for e in l.events]}


@api.route('/legacy/<int:legacy_id>/events/<int:id>', methods=['GET'])
@token_auth.login_required
@json
def get_event(legacy_id, id):  # pylint: disable=I0011,W0622
    """
    Returns single *event* assigned to *legacy* with the given ``id``.

    .. sourcecode:: http

        GET /legacy/1/event/1 HTTP/1.1

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
            "_links": {
                "legacy": "http://127.0.0.1:5000/legacy/1",
                "self": "http://127.0.0.1:5000/legacy/1/events/1"
            },
            "day": 12,
            "description": null,
            "month": 1,
            "name": "Test event 1",
            "status": "ENABLED"
        }


    :statuscode 200: event record included in the response body
    :statuscode 404: no legacy record with given ``id``
    """

    l = Legacy.query.get_or_404(legacy_id)

    if current_app.config.get('IGNORE_AUTH') is not True:  # pragma: no cover
        if not l.can_view(g.user.id):
            raise Http403('Access denied')

    e = Event.query.get_or_404(id)

    if e.legacy_id != l.id:
        raise Http403('Access denied')

    return e


@api.route('/legacy/<int:legacy_id>/events', methods=['POST'])
@token_auth.login_required
@json
def add_event(legacy_id):  # pylint: disable=I0011,W0622
    """
    Add event to an existing *legacy* with the given ``id``.

    .. sourcecode:: http

        POST /legacy/1/events HTTP/1.1
        Content-Type: application/json

        {
        }

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {}


    :statuscode 201: new record created, url included in the `Location` header
    :statuscode 404: no legacy record with given ``id``
    """

    l = Legacy.query.get_or_404(legacy_id)

    if current_app.config.get('IGNORE_AUTH') is not True:  # pragma: no cover
        if l.owner_id != g.user.id:
            raise Http403('Access denied')

        if not l.can_modify(g.user.id):
            raise Http403('Access denied')

    e = Event()
    e.from_dict(request.json)
    e.legacy = l
    e.save()

    return {}, 201, {'Location': e.url()}


@api.route('/legacy/<int:legacy_id>/events/<int:id>', methods=['PUT'])
@token_auth.login_required
@json
def edit_event(legacy_id, id):  # pylint: disable=I0011,W0622
    """
    Modify event of an existing *legacy* with the given ``id``.

    .. sourcecode:: http

        PUT /legacy/1/events/1 HTTP/1.1
        Content-Type: application/json

        {
            "name": "Change Event",
            "description": "...."
        }

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {}


    :statuscode 200: record modified
    :statuscode 400: No/Incomplete/Bad value(s) given in the request body
    :statuscode 404: no legacy record with given ``id``
    """

    l = Legacy.query.get_or_404(legacy_id)

    if current_app.config.get('IGNORE_AUTH') is not True:  # pragma: no cover
        if l.owner_id != g.user.id:
            raise Http403('Access denied')

        if not l.can_modify(g.user.id):
            raise Http403('Access denied')

    e = Event.query.get_or_404(id)

    if e.legacy_id != l.id:
        raise Http403('Access denied')

    e.from_dict(request.json)
    e.save()

    return {}


@api.route('/legacy/<int:legacy_id>/events/<int:id>', methods=['DELETE'])
@token_auth.login_required
@json
def remove_event(legacy_id, id):  # pylint: disable=I0011,W0622
    """
    Remove event from an existing *legacy* with the given ``id``.

    .. sourcecode:: http

        DELETE /legacy/1/event/1 HTTP/1.1
        Content-Type: application/json


    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {}


    :statuscode 200: record deleted
    :statuscode 404: no legacy record with given ``id``
    """

    l = Legacy.query.get_or_404(legacy_id)

    if current_app.config.get('IGNORE_AUTH') is not True:  # pragma: no cover
        if l.owner_id != g.user.id:
            raise Http403('Access denied')

        if not l.can_modify(g.user.id):
            raise Http403('Access denied')

    e = Event.query.get_or_404(id)

    try:
        db.session.delete(e)
        db.session.commit()
    except IntegrityError as e:  # pragma: no cover
        raise IncompleteData('Unable to delete ' + e.__class__.__name__ +
                             ': ' + e.args[0])

    return {}
