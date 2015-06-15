""" Event data model """

from flask import url_for

from . import APIModel
from .. import db
from ..exceptions import IncorrectData


event_status = [
    'ENABLED',
    'DISABLED'
]


event_messages = db.Table('flapi_event_messages',
                          db.Column('event_id', db.Integer,
                                    db.ForeignKey('flapi_event.id')),
                          db.Column('attachment_id', db.Integer,
                                    db.ForeignKey('flapi_attachment.id')))

event_photos = db.Table('flapi_event_photos',
                        db.Column('event_id', db.Integer,
                                  db.ForeignKey('flapi_event.id')),
                        db.Column('attachment_id', db.Integer,
                                  db.ForeignKey('flapi_attachment.id')))


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

    messages = db.relationship('Attachment', secondary=event_messages,
                               backref=db.backref('message_event',
                                                  uselist=False))
    photos = db.relationship('Attachment', secondary=event_photos,
                             backref=db.backref('photo_event', uselist=False))

    def url(self):
        """ Return the HTTP GET URL for this object """

        return url_for('api.get_event', id=self.id, legacy_id=self.legacy_id,
                       _external=True)

    def from_dict(self, data):
        """
        Initialize object instance with data in the given dictionary
        """

        if data is not None and 'status' in data \
                and data['status'] not in event_status:
            raise IncorrectData('Status \'' + data['status']
                                + '\' is not valid')

        super().from_dict(data)  # pylint: disable=I0011,E1004

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