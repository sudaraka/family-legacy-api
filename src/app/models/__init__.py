""" Data Models """


class SerializeAPI(object):
    """ Shared methods to convert object from/to Python dictionary """

    def to_dict(self):
        """ Return current instance converted to Python a dictionary """

        return {k: v for k, v in self.__dict__.items() if k[0] != '_'}


from .person import Person
