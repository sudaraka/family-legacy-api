#!/usr/bin/env sh
# launch-staging-vm.sh: load/build VirtualBox modules and start VM

LOGFILE='/tmp/.vmlog'

echo "========= `date` ========="  >> $LOGFILE

sudo modprobe vboxdrv 2>>$LOGFILE && \
    sudo modprobe vboxpci 2>>$LOGFILE && \
    sudo modprobe vboxnetadp 2>>$LOGFILE && \
    sudo modprobe vboxnetflt 2>>$LOGFILE

if [ 0 -ne $? ]; then
    KERNEL_MODULE="`find /usr/src -type d -name 'vboxhost*' -exec basename {} \;|sed 's/-/\//'`"

    echo "Building VirtualBox kernel module $KERNEL_MODULE"

    sudo dkms uninstall $KERNEL_MODULE >>$LOGFILE 2>&1
    sudo dkms install $KERNEL_MODULE >>$LOGFILE 2>&1

    sudo modprobe vboxdrv 2>>$LOGFILE && \
        sudo modprobe vboxpci 2>>$LOGFILE && \
        sudo modprobe vboxnetadp 2>>$LOGFILE && \
        sudo modprobe vboxnetflt 2>>$LOGFILE

    if [ 0 -ne $? ]; then
        echo 'Failed to load VirtualBox kernel modules.'

        exit 1;
    fi
fi

VM_NAME='FL Staging Server'

if [ -z "`VBoxManage list vms|grep \"$VM_NAME\"`" ]; then
    echo "Virtual machine with name '$VM_NAME' not found"

    exit 1
fi

if [ ! -z "`VBoxManage list runningvms|grep \"$VM_NAME\"`" ]; then
    echo 'Virtual machine is already running.'
else
    VBoxManage startvm "$VM_NAME" --type headless >>$LOGFILE 2>&1

    if [ 0 -ne $? ]; then
        echo 'Failed to start virtual machine'

        exit 1;
    fi

    echo 'Virtual machine started!'

    sudo dhcpcd -qb vboxnet0
fi
