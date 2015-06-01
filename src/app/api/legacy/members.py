""" members API resource """

import re

from flask import g, current_app, request

from .. import api, token_auth
from ...models import Legacy, Person
from ...decorators import json
from ...exceptions import IncompleteData, IncorrectData


# === Resource CRUD ============================================================

@api.route('/legacy/<int:id>/members', methods=['GET'])
@token_auth.login_required
@json
def get_members(id):  # pylint: disable=I0011,W0622
    """
    Returns list of member information of *legacy* with the given ``id``.

    .. sourcecode:: http

        GET /legacy/1/members HTTP/1.1

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
            "members": [
                {
                    "avatar": null,
                    "email": "jdoe@example.com",
                    "first_name": "John",
                    "id": 1,
                    "last_name": "Doe",
                },
                ...
            ]
        }


    :statuscode 200: member records included in the response body
    :statuscode 404: no legacy record with given ``id``
    """

    l = Legacy.query.get_or_404(id)

    if current_app.config.get('IGNORE_AUTH') is not True:
        assert l.can_view(g.user.id), 'Access denied'

    return {'members': [m.to_dict(public_only=True) for m in l.members]}


@api.route('/legacy/<int:id>/members', methods=['POST'])
@token_auth.login_required
@json
def add_members(id):  # pylint: disable=I0011,W0622
    """
    Add member to an existing *legacy* with the given ``id``.

    .. sourcecode:: http

        POST /legacy/1/members HTTP/1.1
        Content-Type: application/json

        {
            "members": [
                <id|email>,
                ...
            ]
        }

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {}


    :statuscode 200: record modified
    :statuscode 202: member invited/notified and awaiting confirmation
    :statuscode 404: no legacy record with given ``id``
    """

    l = Legacy.query.get_or_404(id)

    if current_app.config.get('IGNORE_AUTH') is not True:
        assert l.owner_id == g.user.id, 'Access denied'
        assert l.can_modify(g.user.id), 'Access denied'

    if request.json is None or 'members' not in request.json:
        raise IncompleteData('"members" was not specified')

    member_list = request.json['members']

    if not isinstance(member_list, list):
        raise IncorrectData('"members" is not a valid list')

    for member in member_list:
        member = str(member)

        if not bool(re.match(r'^\d+$', member)):
            member = Person.query.filter_by(email=member).first()

            if member is None:
                # TODO: Invite member
                # TODO: Queue a task to assign member on signup

                return {}, 202
        else:
            member = Person.query.get(member)

            if member is None:
                raise IncorrectData('Member not found')

        # TODO: Queue a task to assign member on acceptance

        # TODO: Remove following after member confirmation is done
        l.members.append(member)

    # TODO: Remove following after member confirmation is done
    l.save()

    return {}


@api.route('/legacy/<int:id>/members', methods=['DELETE'])
@token_auth.login_required
@json
def remove_members(id):  # pylint: disable=I0011,W0622
    """
    Remove members from an existing *legacy* with the given ``id``.

    .. sourcecode:: http

        DELETE /legacy/1/members HTTP/1.1
        Content-Type: application/json

        {
            "members": [
                <id|email>,
                ...
            ]
        }


    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {}


    :statuscode 200: record deleted
    :statuscode 404: no legacy record with given ``id``
    """

    l = Legacy.query.get_or_404(id)

    if current_app.config.get('IGNORE_AUTH') is not True:
        assert l.owner_id == g.user.id, 'Access denied'
        assert l.can_modify(g.user.id), 'Access denied'

    if request.json is None or 'members' not in request.json:
        raise IncompleteData('"members" was not specified')

    member_list = request.json['members']

    if not isinstance(member_list, list):
        raise IncorrectData('"members" is not a valid list')

    for member in member_list:
        member = Person.query.get(member)

        if member is None:
            continue

        l.members.remove(member)

    l.save()

    return {}
