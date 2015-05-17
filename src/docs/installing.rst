.. _installing:

Installing Application
======================

Following instructions assume the current directory is the HOME of user
``flapi``.

Source Code
-----------

Source code is hosted on a private git repository at
`bitbucket.org <https://bitbucket.org/>`_

1. Create SSH key-pair to access bitbucket repository, and upload public key to
   bitbucket.

::

    mkdir .ssh

    ssh-keygen -t rsa -b 4096 -f .ssh/bitbucket.key

    cat<<EOF>.ssh/config
    > host bitbucket
    >   hostname bitbucket.org
    >   user git
    >   identityfile ~/.ssh/bitbucket.key
    > EOF

**Note:** try ``ssh bitbucket`` to verify the connection

2. Clone the repository

::

    git clone --bare bitbucket:sudaraka/family-legacy-api .git

    git config core.bare false

    git reset --hard

    git checkout vx.y.z

**Note:** replace ``vx.y.z`` with the desired version tag


Python 3 Virtual Environment & Dependencies
-------------------------------------------

::

    python3.4 -m venv .virtualenv

    . .virtualenv/bin/activate

    pip install -r requirements/production.txt


Setup Daemon
------------

::

    ln -sv /home/flapi/bin/flapid.sh /etc/init.d/flapid

    chkconfig flapid on


Setup Apache
------------

Make sure Apache include proxy module, or rebuild Apache via CWP and include the
module.

::

    sed \
        -e 's/%HOME%/\/home\/flapi/' \
        -e 's/%DOMAIN%/api.ourfamilylegacy.org/' \
        -e 's/%IP%/69.64.76.150/' \
        /home/flapi/etc/apache.conf > /usr/local/apache/conf.d/flapi.conf
