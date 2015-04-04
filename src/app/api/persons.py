""" persons API resource """

from flask import request

from . import api
from ..models import Person
from ..decorators import json


@api.route('/persons/<int:id>', methods=['GET'])
@json
def get_person(id):  # pylint: disable=I0011,W0622
    """
    Returns single person with the given ``id``.

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
            "email": "persom1@example.com",
            "first_name": "First Name",
            "id": 1,
            "last_name": "Last Name",
            "status": "UNPAID"
        }


    :statuscode 200: person record included in the response body
    :statuscode 404: no person record with given ``id``
    """

    return Person.query.get_or_404(id)


@api.route('/persons/', methods=['POST'])
@json
def create_person():  # pylint: disable=I0011,W0622
    """
    """

    p = Person()
    p.from_dict(request.json)
    p.save()

    return {}, 201, {'Location': p.url()}


@api.route('/persons/<int:id>', methods=['PUT'])
@json
def edit_person(id):  # pylint: disable=I0011,W0622
    """
    """

    p = Person.query.get_or_404(id)
    p.from_dict(request.json)
    p.save()

    return {}
