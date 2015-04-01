#!/usr/bin/env sh
# provision.sh: install software dependencies and setup environment to host the application

if [ "`id -u`" != 0 ]; then
    echo 'Please run this script as root.'

    exit 1
fi

echo 'Family Legacy API - Server Provisioning'
echo '---------------------------------------'
echo ''

# Update system

echo 'Updating packages'

yum update -y -q

echo ''


# Install Python 3 from software collections

echo 'Installing SCL utilities...'
yum install -y -q scl-utils centos-release-SCL

echo ''

echo 'Installing Python 3...'
yum install -y -q python33
scl enable python33 'easy_install -q pip'
echo "`scl enable python33 'python --version'` installed."

echo ''


# Setup user for the application

USER='flapi'

id $USER >/dev/null 2>&1

if [ 0 -ne $? ]; then
    echo "Creating user $USER..."

    adduser -m -s /bin/sh -k /dev/null -U $USER

    if [ 0 -ne $? ]; then
        echo 'Failed to create new user!'

        exit 1;
    fi;
fi;

HOME=`cat /etc/passwd|grep "^$USER:"|cut -d: -f6`

echo ''


echo "Note: install you application to $HOME"

echo 'Done.'
