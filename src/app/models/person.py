""" Person data model """

from flask import url_for

from werkzeug.security import generate_password_hash, check_password_hash

from . import APITokenModel

from .. import db

from ..exceptions import AccessViolation, IncorrectData


person_status = [
    'UNPAID',    # Person registered, but not paid for access to create
    'DISABLED',  # Disabled by administrator or system
    'ACTIVE',    # Person active
    'DECEASED'   # Person was marked by caretaker and confirmed as deceased
]


class Person(db.Model, APITokenModel):
    """ Person data model declarations """

    __tablename__ = 'flapi_persons'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True, index=True)
    status = db.Column(db.Enum(*person_status), default='UNPAID',
                       nullable=False, index=True)

    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    avatar = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))

    def url(self):
        """ Return the HTTP GET URL for this object """

        return url_for('api.get_person', id=self.id, _external=True)

    @property
    def password(self):  # pylint: disable=I0011,R0201
        """ Make password property unreadable """

        raise AccessViolation('Person.password is not readable')

    @password.setter
    def password(self, new_password):
        """ Store hash of the given password """

        self.password_hash = generate_password_hash(new_password)

    def verify_password(self, password):
        """
        Check given password against the current hash and return success/failure
        """

        return check_password_hash(self.password_hash, password)

    def from_dict(self, data):
        """
        Initialize object instance with data in the given dictionary
        """

        if data is not None and 'status' in data \
                and data['status'] not in person_status:
            raise IncorrectData('Status \'' + data['status']
                                + '\' is not valid')

        super().from_dict(data)  # pylint: disable=I0011,E1004

    def to_dict(self):
        """
        Return dictionary created by base class with password hash removed
        """

        result = super().to_dict()  # pylint: disable=I0011,E1004

        if 'password_hash' in result:
            del result['password_hash']

        if 'legacy' in result:
            del result['legacy']

        if 'username' in result:
            del result['username']

        return result
