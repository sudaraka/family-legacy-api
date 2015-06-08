.. _api_person:

Legacy
======

API entry point: ``http://api.ourfamilylegacy.org/legacy/``

**Legacy** resource represent the status of the users (Person) profile.

**Sub-resources**

.. toctree::
    :maxdepth: 1

    api_legacy_owner
    api_legacy_caretaker
    api_legacy_members
    api_legacy_events


----

Status
------

At a given time `legacy` can be in one of the following statuses:

LOCKED
   Legacy profile is either newly created or have passed the lock_date and
   background process archived it.

   Locked legacy profiles can't be modified by anyone.

ACTIVE
   Legacy profile, members, messages and other related elements can be
   modified.

LEGEND
    Legacy owner is deceased and schedules all messages have been send out to
    members.

----

Methods
-------

.. autoflask:: src.app:create_app('dev')
    :undoc-static:
    :blueprints: api
    :endpoints: api.get_legacy
