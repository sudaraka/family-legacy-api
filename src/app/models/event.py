""" Event data model """

from . import APIModel

from .. import db


event_status = [
    'ENABLED',
    'DISABLED'
]


class Event(db.Model, APIModel):
    """ Event data model declarations """

    __tablename__ = 'flapi_event'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum(*event_status), default='ENABLED',
                       nullable=False, index=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text())
    month = db.Column(db.Integer, nullable=False, index=True)
    day = db.Column(db.Integer, nullable=False, index=True)

    # Legacy: many-to-one relationship with Legacy
    legacy_id = db.Column(db.Integer, db.ForeignKey('flapi_legacy.id'))
    legacy = db.relationship('Legacy', backref='events',
                             foreign_keys=[legacy_id])
