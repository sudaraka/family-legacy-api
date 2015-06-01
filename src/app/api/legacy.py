""" legacy API resource """

import re

from flask import request, g

from . import api, token_auth
from ..models import Legacy, Person
from ..decorators import json
from ..exceptions import IncompleteData, IncorrectData


# === Resource CRUD ============================================================

@api.route('/legacy/<int:id>', methods=['GET'])
@token_auth.login_required
@json
def get_legacy(id):  # pylint: disable=I0011,W0622
    """
    Returns single *legacy* with the given ``id``.

    .. sourcecode:: http

        GET /legacy/1 HTTP/1.1

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
            "_links": {
                "self": "/legacy/1",
                "owner": "/person/1",
                "caretaker": "/person/2"
            },
            "archive_hash": null,
            "lock_date": "Fri, 18 Sep 2015 16:19:44 GMT",
            "id": 1,
            "status": "UNPAID"
        }


    :statuscode 200: legacy record included in the response body
    :statuscode 404: no legacy record with given ``id``
    """

    l = Legacy.query.get_or_404(id)

    assert l.can_view(g.user.id), 'Access denied'

    return l


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
    :statuscode 404: no legacy record with given ``id``
    """

    l = Legacy.query.get_or_404(id)

    assert l.owner_id == g.user.id, 'Access denied'
    assert l.can_modify(g.user.id), 'Access denied'

    if 'caretaker' not in request.json:
        raise IncompleteData('"caretaker" was not specified')

    caretaker = request.json['caretaker']

    if not bool(re.match(r'^\d+$', caretaker)):
        caretaker = Person.query.filter_by(email=caretaker).first()

        if caretaker is None:
            # TODO: Invite caretaker
            # TODO: Queue a task to assign caretaker on signup

            return
    else:
        caretaker = Person.query.get(caretaker)

        if caretaker is None:
            raise IncorrectData('Caretaker not found')

    # TODO: Queue a task to assign caretaker on acceptance

    # TODO: Remove following after caretaker confirmation is done
    l.caretaker = caretaker
    l.save()

    return {}
