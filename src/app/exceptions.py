""" Application wide exceptions """


class AccessViolation(Exception):
    """ Attempt to read from restricted model property """
    pass


class NoData(AttributeError):
    """ JSON data is missing in the HTTP request """
    pass


class IncompleteData(ValueError):
    """ JSON data in HTTP request missing required fields """
    pass
