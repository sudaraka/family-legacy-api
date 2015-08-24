""" attachment API resource """

import os

from flask import g, current_app, request

from werkzeug.utils import secure_filename

from sqlalchemy.exc import IntegrityError

from ... import api, token_auth
from .... import db
from ....models import Legacy, Event, Attachment
from ....decorators import json
from ....exceptions import IncompleteData

# === Resource CRUD ============================================================


@api.route('/legacy/<int:legacy_id>/events/<int:event_id>/<att_type>',
           methods=['GET'])
@token_auth.login_required
@json
def get_attachments(legacy_id, event_id, att_type):
    """
    Returns list of attachments assigned to *event* and *legacy* with the given
    id.

    .. sourcecode:: http

        GET /legacy/1/events/1/messages HTTP/1.1

    .. sourcecode:: http

        GET /legacy/1/events/1/photos HTTP/1.1

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
            "messages": [
                {
                    "content_url": "...",
                    "mime_type": "...",
                    "size": 100
                },
                ...
            ]
        }


    :statuscode 200: message/photo records included in the response body
    :statuscode 404: no legacy or event record with given id
    """

    assert att_type in ['messages', 'photos'], \
        'Unsupported attachment type "{}"'.format(att_type)

    l = Legacy.query.get_or_404(legacy_id)

    if current_app.config.get('IGNORE_AUTH') is not True:
        assert l.can_view(g.user.id), 'Access denied'  # pragma: no cover

    e = Event.query.get_or_404(event_id)

    attachments = getattr(e, att_type)

    return {att_type: [att.to_dict() for att in attachments]}


@api.route('/legacy/<int:legacy_id>/events/<int:event_id>/<att_type>',
           methods=['POST'])
@token_auth.login_required
@json
def add_attachment(legacy_id, event_id, att_type):
    """
    Add message/photo to an existing *legacy*/*event* with the given id.

    .. sourcecode:: http

        POST /legacy/1/events/1/messages HTTP/1.1

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {}


    :statuscode 200: record modified
    :statuscode 404: no legacy/event record with given id
    """

    assert att_type in ['messages', 'photos'], \
        'Unsupported attachment type "{}"'.format(att_type)

    uploaded_file = request.files.get('file', None)

    assert uploaded_file is not None, 'File was not uploaded'

    l = Legacy.query.get_or_404(legacy_id)

    if current_app.config.get('IGNORE_AUTH') is not True:  # pragma: no cover
        assert l.owner_id == g.user.id, 'Access denied'
        assert l.can_modify(g.user.id), 'Access denied'

    e = Event.query.get_or_404(event_id)
    attachments = getattr(e, att_type)

    # Find file size using length of the content in the BytesIO stream in
    # uploaded_file.
    #   1. Goto end of the stream
    #   2. Read current position (in bytes from the begining, a.k.a length)
    #   3. Reset stream pointer to start of the stream (other wise the saved
    #      file will be empty).
    uploaded_file.stream.seek(0, 2)
    file_size = uploaded_file.stream.tell()
    uploaded_file.stream.seek(0, 0)

    uploaded_file.filename = secure_filename(uploaded_file.filename)

    a = Attachment(content_url=uploaded_file.filename,
                   mime_type=uploaded_file.mimetype, size=file_size)

    attachments.append(a)

    e.save()

    save_path = os.path.join(current_app.config.get('CONTENT_DIR'),
                             'legacy-{}'.format(l.id),
                             'event-{}'.format(e.id),
                             att_type)
    try:
        os.makedirs(save_path)
    except OSError:
        pass

    uploaded_file.save(os.path.join(save_path, '{}#{}'.format(
        str(a.id),
        uploaded_file.filename
    )))

    return {}


@api.route('/legacy/<int:legacy_id>/events/<int:event_id>/<att_type>/<int:id>',
           methods=['DELETE'])
@token_auth.login_required
@json
# pylint: disable=I0011,W0622
def remove_attachment(legacy_id, event_id, att_type, id):
    """
    Remove message/photo from an existing *legacy*/*event* with the given id.

    .. sourcecode:: http

        DELETE /legacy/1/events/messages/1 HTTP/1.1

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {}


    :statuscode 200: record deleted
    :statuscode 404: no legacy/event record with given id
    """

    assert att_type in ['messages', 'photos'], \
        'Unsupported attachment type "{}"'.format(att_type)

    l = Legacy.query.get_or_404(legacy_id)

    if current_app.config.get('IGNORE_AUTH') is not True:  # pragma: no cover
        assert l.owner_id == g.user.id, 'Access denied'
        assert l.can_modify(g.user.id), 'Access denied'

    # TODO: Delete file from disk

    e = Event.query.get_or_404(event_id)
    a = Attachment.query.get_or_404(id)

    try:
        db.session.delete(a)
        db.session.commit()
    except IntegrityError as e:
        raise IncompleteData('Unable to delete ' + e.__class__.__name__ +
                             ': ' + e.args[0])

    return {}
