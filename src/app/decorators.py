""" Function decorators """

import functools
import hashlib

from flask import jsonify, make_response, request


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
        #   {...}
        #
        # Here we unpack it for further processing
        if isinstance(result, tuple):
            result, status, headers = result + (None, ) * (3 - len(result))

        # At this point if the result is not a dict assume it's a data model
        # object, and call it's to_dict to obtain the result dictionary
        if not isinstance(result, dict):
            result = result.to_dict()

        response = jsonify(result)

        if status is not None:
            response.status_code = status

        if headers is not None:
            response.headers.extend(headers)

        return response

    return wrapped


def etag(f):
    """ Add ETag HTTP header to the response of route """

    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        """ wrap route function """

        rv = make_response(f(*args, **kwargs))

        # ETag is only supported in responses to HTTP GET and HEAD requests
        if request.method not in ['HEAD', 'GET']:
            return rv

        # Make sure we have a valid Flask response object to work with
        response = make_response(rv)

        # Don't generate Etag for errors
        if 200 != response.status_code:
            return response

        _etag = '"' + hashlib.md5(response.get_data()).hexdigest() + '"'
        response.headers['ETag'] = _etag

        if_match = request.headers.get('If-Match')
        if_none_match = request.headers.get('If-None-Match')

        if if_match:
            # Only return the actual response if the generated ETag IS IN the
            # list of ETags sent in request headers.

            etag_list = [t.strip() for t in if_match.split(',')]

            if _etag not in etag_list and '*' not in etag_list:
                response = jsonify({})
                response.status_code = 412  # Precondition Failed
        elif if_none_match:
            # Only return the actual response if the generated ETag IS NOT IN
            # the list of ETags sent in request headers.

            etag_list = [t.strip() for t in if_none_match.split(',')]

            if _etag in etag_list or '*' in etag_list:
                response = jsonify({})
                response.status_code = 304  # Not Modified

        return response

    return wrapped


def cache_control(*directives):
    """ Add Cache-Control HTTP headers to the response """

    def decorator(f):
        """ wrap decorator """

        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            """ wrap route function """

            rv = make_response(f(*args, **kwargs))

            rv.headers['Cache-Control'] = ', '.join(directives)

            return rv

        return wrapped
    return decorator


def no_cache(f):
    """ Shorthand function for inserting no-cache HTTP headers """

    return cache_control('private', 'no-cache', 'no-store', 'max-age=0')(f)
