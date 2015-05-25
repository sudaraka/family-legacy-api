""" legacy API resource """

from flask import g

from . import api, token_auth
from ..models import Legacy
from ..decorators import json


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
