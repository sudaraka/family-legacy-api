#!/bin/sh
#
# flapid: Family Legacy API daemon
#
# chkconfig: 345 85 15
# description: Family Legacy API daemon
# processname: flapid

USER='flapi'

id $USER >/dev/null 2>&1

if [ 0 -ne $? ]; then
    echo "User '$USER' not found."

    exit 1
fi

HOME=`cat /etc/passwd|grep "^$USER:"|cut -d: -f6`

case "$1" in
	start)
		echo 'Starting flapid service'

        supervisord -c $HOME/etc/supervisord.conf -d $HOME
		;;
	stop)
		echo 'Stopping flapid service'

        supervisorctl -c $HOME/etc/supervisord.conf shutdown
		;;
    restart)
		echo 'Restarting flapid service'

        supervisorctl -c $HOME/etc/supervisord.conf restart all
        ;;
	*)
		echo 'Usage: service flapid {start|stop}'

		exit 1
esac

exit 0
