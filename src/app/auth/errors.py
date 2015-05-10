""" Support code for error responses """

from flask import jsonify


def unauthorized():
    """ Return the error response as a JSON """

    response = jsonify({
        'status': 401,
        'error': 'unauthorized',
        'message': 'Authentication credentials missing or invalid'
    })

    response.status_code = 401

    return response
