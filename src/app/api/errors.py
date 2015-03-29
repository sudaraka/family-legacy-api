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


@api.app_errorhandler(500)
def http_internal_server_error(e):
    """ Return HTTP 500 response """

    return jsonify({
        'status': 500,
        'error': 'internal server error',
        'message': e.args[0]
    }), 500
