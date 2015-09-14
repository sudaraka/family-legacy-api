""" Application wide exceptions """


class IncorrectData(AttributeError):
    """ JSON data given in the HTTP request is not acceptable """
    pass


class NoData(AttributeError):
    """ JSON data is missing in the HTTP request """
    pass


class IncompleteData(ValueError):
    """ JSON data in HTTP request missing required fields """
    pass


class CanNotAcceptPayment(Exception):
    """
    User is not in a state (ACTIVE not UNPAID) that system can access payment
    """
    pass


class Http403(Exception):
    """ Throwable exception that will cause API call to return HTTP 403 """
    pass


class Unpaid(Http403):
    """ Not payment record found in the log """
    pass


class AccessViolation(Http403):
    """ Attempt to read from restricted model property """
    pass
