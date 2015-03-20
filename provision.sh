#!/usr/bin/env sh
# provision.sh: install software dependencies and setup environment to host the application

if [ "`id -u`" != 0 ]; then
    echo 'Please run this script as root.'

    exit 1
fi

echo 'Family Legacy API - Server Provisioning'
echo '---------------------------------------'
echo ''

# Install Python 3 from software collections

echo 'Installing SCL utilities...'
yum install -y -q scl-utils centos-release-SCL >/dev/null

echo 'Installing Python 3...'
yum install -y -q python33 >/dev/null
scl enable python33 'easy_install -q pip 2>/dev/null'
echo "`scl enable python33 'python --version'` installed."

echo ''


echo 'Done.'
