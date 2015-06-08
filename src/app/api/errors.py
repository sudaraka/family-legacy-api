""" API routes and support code for error responses """

from flask import jsonify

from sqlalchemy.exc import OperationalError

from . import api
from ..exceptions import IncompleteData, NoData, IncorrectData
from ..exceptions import CanNotAcceptPayment
from ..decorators import no_cache


@api.app_errorhandler(404)
@no_cache
def http_not_found(e):
    """ Return HTTP 404 response """

    return jsonify({
        'status': 404,
        'error': 'not found',
        'message': 'Requested resource does not exists'
    }), 404


@api.app_errorhandler(405)
@no_cache
def http_method_not_allowed(e):
    """ Return HTTP 405 response """

    return jsonify({
        'status': 405,
        'error': 'method not allowed',
        'message': 'Resource does not support the requested method'
    }), 405


@api.app_errorhandler(500)
@no_cache
def http_internal_server_error(e):
    """ Return HTTP 500 response """

    return jsonify({  # pragma: no cover
        'status': 500,
        'error': 'internal server error',
        'message': e.args[0]
    }), 500


@api.app_errorhandler(NoData)
@api.app_errorhandler(IncompleteData)
@api.app_errorhandler(IncorrectData)
@no_cache
def exception_incomplete_data(e):
    """ Return HTTP 400 response when missing or no modal data """

    return jsonify({
        'status': 400,
        'error': 'bad request',
        'message': e.args[0]
    }), 400


@api.app_errorhandler(OperationalError)
@no_cache
def exception_database_operation(e):
    """ Return HTTP 500 response for database related errors """

    return jsonify({
        'status': 500,
        'error': 'database operation failed',
        'message': e.args[0]
    }), 500


@api.app_errorhandler(AssertionError)
@no_cache
def exception_assert(e):
    """ Return HTTP 403 response when assertion is met """

    return jsonify({
        'status': 403,
        'error': 'forbidden',
        'message': str(e)
    }), 403


@api.app_errorhandler(CanNotAcceptPayment)
@no_cache
def cannot_pay_exception(e):
    """ Return HTTP 405 for unacceptable payments """

    return jsonify({
        'status': 405,
        'error': 'method not allowed',
        'message': 'Current user is not allowed to make a payment'
    }), 405
