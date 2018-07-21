#!/bin/sh

TMPDIR="/tmp"
TMPFILE="${TMPDIR}/`date +%Y%m%d-%H%M%S`.html"

ENVDIR="${HOME}/env"
ACTIVATE="${ENVDIR}/bin/activate"

DSTDIR="ytani@ssh.ytani.net:public_html/iot"

NETINTERFACES="${HOME}/bin/netinterfaces.py"

#####
if [ ! -f ${ACTIVATE} ]; then
    echo "${ACTIVATE}: not found"
    exit 1
fi

if [ ! -x ${NETINTERFACES} ]; then
    echo ${NETINTERFACES}: not found
fi

#####
. ${ACTIVATE}

${NETINTERFACES} > ${TMPFILE}

scp ${TMPFILE} ${DSTDIR}
rm ${TMPFILE}
