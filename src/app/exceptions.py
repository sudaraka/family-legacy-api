""" Application wide exceptions """


class IncompleteData(ValueError):
    """ JSON data in HTTP request missing required fields """
    pass
