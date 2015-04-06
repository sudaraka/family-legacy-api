#!/usr/bin/env sh
# launch-staging-vm.sh: load/build VirtualBox modules and start VM

LOGFILE='/tmp/.vmlog'

function load_modules() {
    VB_MODULES='vboxdrv vboxpci vboxnetadp vboxnetflt'
    LOAD_ERROR=0

    for MOD in $VB_MODULES; do
        if [ -z "`lsmod|grep ^$MOD`" ]; then
            sudo modprobe $MOD 2>>$LOGFILE

            if [ 0 -ne $? ]; then
                LOAD_ERROR=1
                break
            fi;
        fi;
    done;

    if [ 0 -ne $LOAD_ERROR ]; then
        KERNEL_MODULE="`find /usr/src -type d -name 'vboxhost*' -exec basename {} \;|sed 's/-/\//'`"

        echo "Building VirtualBox kernel module $KERNEL_MODULE"

        sudo dkms uninstall $KERNEL_MODULE >>$LOGFILE 2>&1
        sudo dkms install $KERNEL_MODULE >>$LOGFILE 2>&1

        load_modules

        if [ 0 -ne $? ]; then
            echo 'Failed to load VirtualBox kernel modules.'

            return 1
        fi
    fi

    return 0
}

echo "========= `date` ========="  >> $LOGFILE

load_modules

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

    if [ -z "`ip addr show vboxnet0|grep 'inet 10\.0\.0\.'`" ]; then
        sudo dhcpcd -qb vboxnet0
    fi
fi
