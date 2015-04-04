""" Data Models """


class SerializeAPI(object):
    """ Shared methods to convert object from/to Python dictionary """

    def to_dict(self):
        """ Return current instance converted to Python a dictionary """

        result = {k: v for k, v in self.__dict__.items() if k[0] != '_'}

        result['_links'] = {
            'self': self.url()
        }

        return result


from .person import Person
