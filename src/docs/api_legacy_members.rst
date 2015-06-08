.. _api_person:

Members
=======

API entry point: ``http://api.ourfamilylegacy.org/legacy/<id>/members``

**Members** resource is a pointer to a list of Person profiles that are members
of the Legacy. These Person records have limited information and access rights.

----


Methods
-------

.. autoflask:: src.app:create_app('dev')
    :undoc-static:
    :blueprints: api
    :endpoints: api.get_members, api.add_members, api.remove_members
