""" Application wide exceptions """


class NoData(AttributeError):
    """ JSON data is missing in the HTTP request """
    pass


class IncompleteData(ValueError):
    """ JSON data in HTTP request missing required fields """
    pass
