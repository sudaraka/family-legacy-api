.. _api_person:

Photos
======

API entry point:
``http://api.ourfamilylegacy.org/legacy/<id>/events/<id>/photos``

**Photos** for the event

----


Methods
-------

.. autoflask:: src.app:create_app('dev')
    :undoc-static:
    :blueprints: api
    :endpoints: api.get_attachments, api.add_attachment, api.remove_attachment
