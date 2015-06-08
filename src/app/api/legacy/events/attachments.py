""" attachment API resource """

from flask import g, current_app

from ... import api, token_auth
from ....models import Legacy, Event
from ....decorators import json

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
        assert l.can_view(g.user.id), 'Access denied'

    e = Event.query.get_or_404(event_id)

    attachments = getattr(e, att_type)

    return {att_type: [att.to_dict() for att in attachments]}

