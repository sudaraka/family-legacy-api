""" Data Models """

from sqlalchemy.exc import IntegrityError

from .. import db
from ..exceptions import NoData, IncompleteData


class APIModel(object):
    """ Shared methods to convert object from/to Python dictionary """

    def from_dict(self, data):
        """
        Initialize object instance with data in the given dictionary
        """

        try:
            for field, value in data.items():
                if 'id' == field:  # Ignore id fields (primary key)
                    continue

                setattr(self, field, value)
        except AttributeError:
            raise NoData('No data given to create ' + self.__class__.__name__)

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
