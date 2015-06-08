.. _api_person:

Owner
=====

API entry point: ``http://api.ourfamilylegacy.org/legacy/<id>/owner``

**Owner** resource is a pointer to the Person profile the Legacy belongs
to, but with limited information and access rights.

----


Methods
-------

.. autoflask:: src.app:create_app('dev')
    :undoc-static:
    :blueprints: api
    :endpoints: api.get_owner
