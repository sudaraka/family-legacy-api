""" Authenticate by Person credentials """

from flask import g
from flask.ext.httpauth import HTTPBasicAuth

from . import auth
from .errors import unauthorized
from ..decorators import json
from ..models.person import Person


http_auth = HTTPBasicAuth()


@http_auth.error_handler
def person_unauthorized():
    """ Handle authentication errors """

    return unauthorized()


@http_auth.verify_password
def verify_password(username, password):
    """ Verify username and password received via HTTP Basic Auth """

    g.user = Person.query.filter_by(email=username).first()

    if g.user is None:
        return None

    return g.user.verify_password(password)


@auth.route('/person')
@http_auth.login_required
@json
def auth_person():  # pylint: disable=I0011,W0622
    """
    Authenticate user based on Person credentials

    .. sourcecode:: http

        GET /auth/person HTTP/1.1

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
            "token": "..."
        }


    :statuscode 200: token for authenticate API calls for the session included
    in the response body
    :statuscode 403: authentication failed
    """

    return {
        'id': g.user.id,
        'token': g.user.get_token()
    }
