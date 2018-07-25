#!/bin/sh

MYNAME=`basename $0`

BINDIR=${HOME}/bin
SCP_IPADDR=${BINDIR}/scp_ipaddr.sh

if [ ! -x ${SCP_IPADDR} ]; then
    echo "${SCP_IPADDR}: not found"
    exit 1
fi

${SCP_IPADDR} &
