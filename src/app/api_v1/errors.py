""" API routes and support code for error responses """

from flask import jsonify

from . import api


@api.app_errorhandler(404)
def http_not_found(e):
    """ Return HTTP 404 response """

    return jsonify({
        'status': 404,
        'error': 'not found',
        'message': 'Requested resource does not exists'
    }), 404
