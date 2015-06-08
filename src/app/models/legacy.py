""" Legacy data model """

from flask import url_for

from . import APIModel

from .. import db


legacy_status = [
    'ACTIVE',
    'LOCKED',
    'LEGEND'
]

members = db.Table('flapi_legacy_members',
                   db.Column('legacy_id', db.Integer,
                             db.ForeignKey('flapi_legacy.id')),
                   db.Column('member_id', db.Integer,
                             db.ForeignKey('flapi_persons.id')))


class Legacy(db.Model, APIModel):
    """ Legacy data model declarations """

    __tablename__ = 'flapi_legacy'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum(*legacy_status), default='LOCKED',
                       nullable=False, index=True)
    lock_date = db.Column(db.DateTime)
    archive_hash = db.Column(db.String(40))

    # Owner: one-to-one relationship with Person
    owner_id = db.Column(db.Integer, db.ForeignKey('flapi_persons.id'),
                         nullable=False, unique=True)
    owner = db.relationship('Person', uselist=False, backref='legacy',
                            foreign_keys=[owner_id])

    # Caretaker: many-to-one relationship with Person
    caretaker_id = db.Column(db.Integer, db.ForeignKey('flapi_persons.id'))
    caretaker = db.relationship('Person', foreign_keys=[caretaker_id])

    # Members: many-to-many relationship with Person
    members = db.relationship('Person', secondary=members)

    def url(self):
        """ Return the HTTP GET URL for this object """

        return url_for('api.get_legacy', id=self.id, _external=True)

    def to_dict(self):
        """
        Return dictionary created by base class with owner, caretaker removed
        from main body and in _links
        """

        result = super().to_dict()  # pylint: disable=I0011,E1004

        if 'owner_id' in result:
            del result['owner_id']

        if 'caretaker_id' in result:
            del result['caretaker_id']

        result['_links']['owner'] = url_for('api.get_owner',
                                            id=self.id, _external=True)

        result['_links']['caretaker'] = url_for('api.get_caretaker',
                                                id=self.id, _external=True)

        result['_links']['members'] = url_for('api.get_members',
                                              id=self.id, _external=True)

        return result

    def can_modify(self, person_id):
        """
        Return whether the person with given id can modify this legacy details
        """

        if 'LEGEND' == self.status:
            # Legacy operations are complete, no one can make changes.

            return False

        if person_id == self.owner_id and 'ACTIVE' == self.status:
            # Owner can modify active Legacy

            return True

        if person_id == self.caretaker_id and 'DECEASED' == self.owner.status:
            # Caretaker can modify Legacy only when owner is deceased

            return True

        # Other can't modify
        return False

    def can_view(self, person_id):
        """
        Return whether the person with given id can read this legacy details
        """

        if person_id == self.owner_id:
            # Owner can view

            return True

        if person_id == self.caretaker_id:
            # Caretaker can view

            return True

        if True in [person_id == m.id for m in self.members]:
            # Members can view

            return True

        # Other can't view
        return False
