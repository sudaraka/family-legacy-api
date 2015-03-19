#!/usr/bin/env sh

LOGFILE='/tmp/.vmlog'

echo "========= `date` ========="  >> $LOGFILE

sudo modprobe vboxdrv 2>$LOGFILE && \
    sudo modprobe vboxpci 2>$LOGFILE && \
    sudo modprobe vboxnetadp 2>$LOGFILE && \
    sudo modprobe vboxnetflt 2>$LOGFILE

if [ 0 -ne $? ]; then
    KERNEL_MODULE="`find /usr/src -type d -name 'vboxhost*' -exec basename {} \;|sed 's/-/\//'`"

    echo 'Building VirtualBox kernel modules...'

    sudo dkms uninstall $KERNEL_MODULE >$LOGFILE 2>&1
    sudo dkms install $KERNEL_MODULE >$LOGFILE 2>&1

    sudo modprobe vboxdrv 2>$LOGFILE && \
        sudo modprobe vboxpci 2>$LOGFILE && \
        sudo modprobe vboxnetadp 2>$LOGFILE && \
        sudo modprobe vboxnetflt 2>$LOGFILE

    if [ 0 -ne $? ]; then
        echo 'Failed to load VirtualBox kernel modules.'

        exit 1;
    fi
fi

VMID="`VBoxManage list vms|grep 'FL Staging'|cut -d'{' -f2|cut -d'}' -f1`"

if [ -z "$VMID" ]; then
    echo 'Virtual machine with name "FL Staging" not found'

    exit 1
fi

if [ ! -z "`VBoxManage list runningvms|grep '$VMID'`" ]; then
    echo 'Virtual machine is already running.'
else
    VBoxManage startvm $VMID --type headless >$LOGFILE 2>&1

    if [ 0 -ne $? ]; then
        echo 'Failed to start virtual machine'

        exit 1;
    fi

    echo 'Virtual machine started!'

    sudo dhcpcd -qb vboxnet0
fi
