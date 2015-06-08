""" Attachment data model """

from flask import url_for

from . import APIModel
from .. import db


class Attachment(db.Model, APIModel):
    """ Attachment data model declarations """

    __tablename__ = 'flapi_attachment'

    id = db.Column(db.Integer, primary_key=True)
    content_url = db.Column(db.String(150), nullable=False)
    mime_type = db.Column(db.String(50))
    size = db.Column(db.Integer, nullable=False)

    def url(self):
        """ Return the HTTP GET URL for this object """

        att_type = 'messages'
        event = self.message_event

        if event is None:
            att_type = 'photos'
            event = self.photo_event

        return url_for('api.remove_attachment', id=self.id, att_type=att_type,
                       legacy_id=event.legacy_id, event_id=event.id,
                       _external=True)
