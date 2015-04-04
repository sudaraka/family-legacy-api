""" Data Models """

from sqlalchemy.exc import IntegrityError

from .. import db
from ..exceptions import IncompleteData


class SerializeAPI(object):
    """ Shared methods to convert object from/to Python dictionary """

    def to_dict(self):
        """ Return current instance converted to Python a dictionary """

        result = {k: v for k, v in self.__dict__.items() if k[0] != '_'}

        result['_links'] = {
            'self': self.url()
        }

        return result

    def save(self):
        """ Save/commit changed of current instance to DB """

        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            raise IncompleteData('Unable to save ' + self.__class__.__name__ +
                                 ': ' + e.args[0])


from .person import Person
