""" persons API resource """

from flask import request, g, current_app

from . import api, token_auth
from ..models import Person
from ..decorators import json


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
        assert id == g.user.id, 'Access denied'

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
        assert id == g.user.id, 'Access denied'

    p = Person.query.get_or_404(id)
    p.from_dict(request.json)
    p.save()

    return {}
