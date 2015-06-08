.. _api_person:

Events
======

API entry point: ``http://api.ourfamilylegacy.org/legacy/<id>/events``

**Events** created by the owner of the Legacy that will play out after the death
of the owner.

----


Methods
-------

.. autoflask:: src.app:create_app('dev')
    :undoc-static:
    :blueprints: api
    :endpoints: api.get_events, api.get_event, api.add_event, api.edit_event,
        api.remove_event
