""" owner API resource """

from flask import g, current_app

from .. import api, token_auth
from ...models import Legacy
from ...decorators import json


# === Resource CRUD ============================================================

@api.route('/legacy/<int:id>/owner', methods=['GET'])
@token_auth.login_required
@json
def get_owner(id):  # pylint: disable=I0011,W0622
    """
    Returns owner information of *legacy* with the given ``id``.

    .. sourcecode:: http

        GET /legacy/1/owner HTTP/1.1

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


    :statuscode 200: owner record included in the response body
    :statuscode 404: no legacy record with given ``id``
    """

    l = Legacy.query.get_or_404(id)

    if current_app.config.get('IGNORE_AUTH') is not True:
        assert l.can_view(g.user.id), 'Access denied'

    return l.owner.to_dict(public_only=True)
