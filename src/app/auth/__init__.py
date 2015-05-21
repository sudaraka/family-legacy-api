""" API Blueprint """

from flask import Blueprint

from ..decorators import no_cache


auth = Blueprint('auth', __name__)


@auth.after_request
@no_cache
def after_request(response):
    """
    Apply CORS, no-cache Cache-Control headers HTTP responses generated by this
    blueprint
    """

    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'authorization'

    return response


from . import person, errors