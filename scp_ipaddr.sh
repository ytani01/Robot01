#!/bin/sh

MYNAME=`basename $0`

DSTDIR="ytani@ssh.ytani.net:public_html/iot"

TMPDIR="/tmp"
TMPFILE="${TMPDIR}/`date +%Y%m%d-%H%M%S`.html"
TMPFILE_PREV="${TMPDIR}/${MYNAME}.prev"

ENVDIR="${HOME}/env"
ACTIVATE="${ENVDIR}/bin/activate"

NETINTERFACES="${HOME}/bin/netinterfaces.py 5000"

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

while true; do
    ${NETINTERFACES} > ${TMPFILE}

    if diff ${TMPFILE_PREV} ${TMPFILE}; then
	echo 'not changed'
    else
	scp ${TMPFILE} ${DSTDIR}
	mv ${TMPFILE} ${TMPFILE_PREV}
    fi

    sleep 60
done


