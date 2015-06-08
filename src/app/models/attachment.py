""" Attachment data model """

from . import APIModel
from .. import db


class Attachment(db.Model, APIModel):
    """ Attachment data model declarations """

    __tablename__ = 'flapi_attachment'

    id = db.Column(db.Integer, primary_key=True)
    content_url = db.Column(db.String(150), nullable=False)
    mime_type = db.Column(db.String(50))
    size = db.Column(db.Integer, nullable=False)
