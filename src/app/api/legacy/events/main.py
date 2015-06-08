""" event API resource """

from flask import g, current_app, request

from ... import api, token_auth
from ....models import Legacy, Event
from ....decorators import json

# === Resource CRUD ============================================================


@api.route('/legacy/<int:legacy_id>/events', methods=['GET'])
@token_auth.login_required
@json
def get_events(legacy_id):  # pylint: disable=I0011,W0622
    """
    Returns all *events* assigned to *legacy* with the given ``id``.

    .. sourcecode:: http

        GET /legacy/1/events HTTP/1.1

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
            "events": [
                {
                    "_links": {
                        "self": "http://127.0.0.1:5000/legacy/1/events/1"
                    },
                    "day": 12,
                    "month": 1,
                    "name": "Test event 1",
                    "status": "ENABLED"
                },
                ...
            ]
        }


    :statuscode 200: event records included in the response body
    :statuscode 404: no legacy record with given ``id``
    """

    l = Legacy.query.get_or_404(legacy_id)

    if current_app.config.get('IGNORE_AUTH') is not True:
        assert l.can_view(g.user.id), 'Access denied'

    return {"events": [e.to_dict(True) for e in l.events]}


@api.route('/legacy/<int:legacy_id>/events/<int:id>', methods=['GET'])
@token_auth.login_required
@json
def get_event(legacy_id, id):  # pylint: disable=I0011,W0622
    """
    Returns single *event* assigned to *legacy* with the given ``id``.

    .. sourcecode:: http

        GET /legacy/1/event/1 HTTP/1.1

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
            "_links": {
                "legacy": "http://127.0.0.1:5000/legacy/1",
                "self": "http://127.0.0.1:5000/legacy/1/events/1"
            },
            "day": 12,
            "description": null,
            "month": 1,
            "name": "Test event 1",
            "status": "ENABLED"
        }


    :statuscode 200: event record included in the response body
    :statuscode 404: no legacy record with given ``id``
    """

    l = Legacy.query.get_or_404(legacy_id)

    if current_app.config.get('IGNORE_AUTH') is not True:
        assert l.can_view(g.user.id), 'Access denied'

    e = Event.query.get_or_404(id)
    assert e.legacy_id == l.id, 'Access denied'

    return e


@api.route('/legacy/<int:legacy_id>/events', methods=['POST'])
@token_auth.login_required
@json
def add_event(legacy_id):  # pylint: disable=I0011,W0622
    """
    Add event to an existing *legacy* with the given ``id``.

    .. sourcecode:: http

        POST /legacy/1/events HTTP/1.1
        Content-Type: application/json

        {
        }

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {}


    :statuscode 201: new record created, url included in the `Location` header
    :statuscode 404: no legacy record with given ``id``
    """

    l = Legacy.query.get_or_404(legacy_id)

    if current_app.config.get('IGNORE_AUTH') is not True:
        assert l.owner_id == g.user.id, 'Access denied'
        assert l.can_modify(g.user.id), 'Access denied'

    e = Event()
    e.from_dict(request.json)
    e.legacy = l
    e.save()

    return {}, 201, {'Location': e.url()}
