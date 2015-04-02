.. _provisioning:

Provision Staging/Production Server
===================================

*Following instructions are based on CentOS 6.6 (x86_64)*

Script ``provision.sh`` included in the source repository can be used to
automate the installation of packages mentioned below and setup all required
deployment for the API application.

Python 3
--------

1. Add `Software Collections <https://www.softwarecollections.org/>`_ support by
   installing **scl-utils** and **centos-release-SCL** packages.

   ``yum install scl-utils centos-release-SCL``

2. Install **python33** package.

   ``yum install python33``

3. Install **pip** via easy_install with python33 SCL is enabled.

   ``scl enable python33 'easy_install pip'``


Git
---

Application will be deployed via **git** (among other things), there for is a
critical part of the target environment.

   ``yum install git``


User
----

Create user and group named **flapi**. API application will be installed into
the home directory of this user and run in the same context.

Note: *this user should have minimal privileges and not remote access.*

    ``adduser -m -s /bin/sh -U flapi``
