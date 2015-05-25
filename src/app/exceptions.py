""" Application wide exceptions """


class AccessViolation(Exception):
    """ Attempt to read from restricted model property """
    pass


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
