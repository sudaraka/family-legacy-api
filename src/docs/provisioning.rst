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
