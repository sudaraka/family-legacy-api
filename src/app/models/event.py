""" Event data model """

from flask import url_for

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

    def url(self):
        """ Return the HTTP GET URL for this object """

        return url_for('api.get_event', id=self.id, legacy_id=self.legacy_id,
                       _external=True)

    def to_dict(self, public_only=False):
        """ Return dictionary created by base class with legacy_id removed """

        if not public_only:
            # Trigger dynamic lazy loading of the legacy
            l = self.legacy

        result = super().to_dict()  # pylint: disable=I0011,E1004

        del result['legacy_id']

        if public_only:
            # Remove private/sensitive information

            del result['description']
        else:
            result['_links']['legacy'] = result['legacy']
            del result['legacy']

        return result
