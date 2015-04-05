.. _provisioning:

Provision Staging/Production Server
===================================

*Following instructions are based on CentOS 6.6 (x86_64)*

Script ``provision.sh`` included in the source repository can be used to
automate the installation of packages mentioned below and setup all required
deployment for the API application.

Python 3
--------

From SCL
^^^^^^^^

1. Add `Software Collections <https://www.softwarecollections.org/>`_ support by
   installing **scl-utils** and **centos-release-SCL** packages.

   ``yum install scl-utils centos-release-SCL``

2. Install **python33** package.

   ``yum install python33``

3. Install **pip** via easy_install with python33 SCL is enabled.

   ``scl enable python33 'easy_install pip'``

From Source
^^^^^^^^^^^

Reference: `Creating your first Linux App with Python 3 and Flask
<http://techarena51.com/index.php/how-to-install-python-3-and-flask-on-linux/>`_

1. Install **development tools** and packages.

   ``yum groupinstall -y 'Development Tools'``

   ``yum install -y zilb-devel openssl-devel sqlite-devel bsip2-devel``

2. Download Python 3.x source from `python.org <https://www.python.org/>`_.

   ``wget https://www.python.org/ftp/python/3.x.x/Python-3.x.x.tar.xz``

   ``tar xf Python-3.x.x.tar.xz``

3. Build & install.

   ``cd Python-3.x.x.tar.xz``

   ``./configure``

   ``make``

   ``make altinstall``


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

    ``adduser -m -s /bin/sh -k /dev/null -U flapi``
