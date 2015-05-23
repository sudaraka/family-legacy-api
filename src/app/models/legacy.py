""" Legacy data model """

from . import APIModel

from .. import db


legacy_status = [
    'ACTIVE',
    'LOCKED'
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

        return ''  # url_for('api.get_legacy', id=self.id, _external=True)
