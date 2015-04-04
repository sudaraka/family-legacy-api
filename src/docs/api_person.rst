.. _api_person:

Person
======

API entry point: ``http://www.ourfamilylegacy.org/api/person/``

**Person** resource represent the registered user of the application which
create an owns a legacy.

----

Status
------

At a given time `person` can be in one of the following statuses:

UNPAID
   Newly registered user and have not yet made a payment to activate the
   account.
   Person **can** **login** and **edit profile** information, but **can not**
   **create legacy** or any legacy related actions.

ACTIVE
   Registered member of the site will full access to all functions of the site.

DISABLED
   Person has been disabled by administrator or system process. Person can't
   login nor any of the legacy operations will be performed on this account by
   the system.

DECEASED
   Caretaker has informed this person as deceased and it has been verified.
   Login to the person account is disabled, however caretaker will have limited
   access.

----

Methods
-------

.. autoflask:: src.app:create_app('dev')
    :undoc-static:
    :blueprints: api
    :endpoints: api.get_person
