""" Function decorators """

import functools

from flask import jsonify


def json(f):
    """ Convert return values to JSON API responses """

    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        """ wrap route function """

        status = None
        headers = None

        # call route handler
        result = f(*args, **kwargs)

        # routes are allowed to return a tuple
        # i.e.
        #   {...}, 200, {'X-Header': ''}
        #   {...}, {'X-Header': '...'}
        #   {...}
        #
        # Here we unpack it for further processing
        if isinstance(result, tuple):
            result, status, headers = result + (None, ) * (3 - len(result))

        if isinstance(status, (dict, list)):
            headers, status = status, None

        # At this point if the result is not a dict assume it's a data model
        # object, and call it's to_dict to obtain the result dictionary
        if not isinstance(result, dict):
            result = result.to_dict()

        response = jsonify(result)

        if status is not None:
            response.status_code = status

        if headers is not None:
            result.headers.extend(headers)

        return response

    return wrapped
