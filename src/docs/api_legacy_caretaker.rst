.. _api_person:

Caretaker
=========

API entry point: ``http://api.ourfamilylegacy.org/legacy/<id>/caretaker``

**Caretaker** resource is a pointer to the Person profile that is the designated
caretaker of the Legacy.This resource only give limited information and access
rights to the actual Person record.

----


Methods
-------

.. autoflask:: src.app:create_app('dev')
    :undoc-static:
    :blueprints: api
    :endpoints: api.get_caretaker, api.edit_caretaker, api.remove_caretaker
