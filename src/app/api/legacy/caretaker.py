""" caretaker API resource """

import re

from flask import request, g, current_app, abort

from .. import api, token_auth
from ...models import Legacy, Person
from ...decorators import json
from ...exceptions import IncompleteData, IncorrectData


# === Resource CRUD ============================================================

@api.route('/legacy/<int:id>/caretaker', methods=['GET'])
@token_auth.login_required
@json
def get_caretaker(id):  # pylint: disable=I0011,W0622
    """
    Returns caretaker information of *legacy* with the given ``id``.

    .. sourcecode:: http

        GET /legacy/1/caretaker HTTP/1.1

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
            "avatar": null,
            "email": "jdoe@example.com",
            "first_name": "John",
            "id": 1,
            "last_name": "Doe",
        }


    :statuscode 200: caretaker record included in the response body
    :statuscode 404: no legacy record with given ``id`` or caretaker not
                     assigned
    """

    l = Legacy.query.get_or_404(id)

    if current_app.config.get('IGNORE_AUTH') is not True:
        assert l.can_view(g.user.id), 'Access denied'  # pragma: no cover

    if isinstance(l.caretaker, Person):
        return l.caretaker.to_dict(public_only=True)

    abort(404)


@api.route('/legacy/<int:id>/caretaker', methods=['PUT'])
@token_auth.login_required
@json
def edit_caretaker(id):  # pylint: disable=I0011,W0622
    """
    Assign caretaker to an existing *legacy* with the given ``id``.

    .. sourcecode:: http

        PUT /legacy/1/caretaker HTTP/1.1
        Content-Type: application/json

        {
            "caretaker": "<id|email>"
        }

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {}


    :statuscode 200: record modified
    :statuscode 202: caretaker invited/notified and awaiting confirmation
    :statuscode 404: no legacy record with given ``id``
    """

    l = Legacy.query.get_or_404(id)

    if current_app.config.get('IGNORE_AUTH') is not True:  # pragma: no cover
        assert l.owner_id == g.user.id, 'Access denied'
        assert l.can_modify(g.user.id), 'Access denied'

    if request.json is None or 'caretaker' not in request.json:
        raise IncompleteData('"caretaker" was not specified')

    caretaker = request.json['caretaker']

    if not bool(re.match(r'^\d+$', caretaker)):
        caretaker = Person.query.filter_by(email=caretaker).first()

        if caretaker is None:
            # TODO: Invite caretaker
            # TODO: Queue a task to assign caretaker on signup

            return {}, 202
    else:
        caretaker = Person.query.get(caretaker)

        if caretaker is None:
            raise IncorrectData('Caretaker not found')

    # TODO: Queue a task to assign caretaker on acceptance

    # TODO: Remove following after caretaker confirmation is done
    l.caretaker = caretaker
    l.save()

    return {}


@api.route('/legacy/<int:id>/caretaker', methods=['DELETE'])
@token_auth.login_required
@json
def remove_caretaker(id):  # pylint: disable=I0011,W0622
    """
    Remove caretaker of an existing *legacy* with the given ``id``.

    .. sourcecode:: http

        DELETE /legacy/1/caretaker HTTP/1.1
        Content-Type: application/json


    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {}


    :statuscode 200: record deleted
    :statuscode 404: no legacy record with given ``id``
    """

    l = Legacy.query.get_or_404(id)

    if current_app.config.get('IGNORE_AUTH') is not True:  # pragma: no cover
        assert l.owner_id == g.user.id, 'Access denied'
        assert l.can_modify(g.user.id), 'Access denied'

    l.caretaker = None
    l.save()

    return {}
