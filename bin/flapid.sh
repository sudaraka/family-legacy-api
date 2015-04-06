#!/bin/sh
#
# flapid: Family Legacy API daemon
#
# chkconfig: 345 85 15
# description: Family Legacy API daemon
# processname: flapid

USER='flapi'
PIDFILE='/var/run/flapid.pid'

id $USER >/dev/null 2>&1

if [ 0 -ne $? ]; then
    echo "User '$USER' not found."

    exit 1
fi

HOME=`cat /etc/passwd|grep "^$USER:"|cut -d: -f6`

case "$1" in
	start)
		echo 'Starting flapid service'

		$HOME/.virtualenv/bin/gunicorn -D \
            -c $HOME/src/app/gunicorn.py \
            -u $USER -g $USER \
            -p $PIDFILE \
            src.app.wsgi:application
		;;
	stop)
		echo 'Stopping flapid service'

		kill `cat $PIDFILE`
		;;
	*)
		echo 'Usage: service flapid {start|stop}'

		exit 1
esac

exit 0

