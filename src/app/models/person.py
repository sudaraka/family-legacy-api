""" Person data model """

from flask import url_for

from . import SerializeAPI

from .. import db

person_status = [
    'UNPAID',    # Person registered, but not paid for access to create
    'DISABLED',  # Disabled by administrator or system
    'ACTIVE',    # Person active
    'DECEASED'   # Person was marked by caretaker and confirmed as deceased
]


class Person(db.Model, SerializeAPI):
    """ Person data model declarations """

    __tablename__ = 'flapi_persons'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum(*person_status), default='UNPAID',
                       nullable=False, index=True)

    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), nullable=False, unique=True, index=True)
    avatar = db.Column(db.String(128))

    def to_dict(self):
        """ Return current instance converted to Python a dictionary """

        result = super().to_dict()

        result['_links'] = {
            'self': url_for('api.get_person', id=self.id, _external=True)
        }

        return result
