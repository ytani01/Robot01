#!/bin/sh
#
MYNAME=`basename $0`

DSTDIR="ytani@ssh.ytani.net:public_html/iot"

NETINTERFACES="${HOME}/bin/netinterfaces.py"
PORTS="5000"

TMPDIR="/tmp"
#TMPFILE="${TMPDIR}/`date +%Y%m%d-%H%M%S`.htm"
TMPFILE="${TMPDIR}/`hostname`.html"
TMPFILE_PREV="${TMPFILE}.prev"

ENVDIR="${HOME}/env"
ACTIVATE="${ENVDIR}/bin/activate"

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

if [ -f ${TMPFILE_PREV} ]; then
    rm -f ${TMPFILE_PREV}
    touch ${TMPFILE_PREV}
fi

while true; do
    SLEEP_SEC=60

    ${NETINTERFACES} ${PORTS} > ${TMPFILE} 2>&1

    if diff ${TMPFILE_PREV} ${TMPFILE}; then
	echo 'not changed'
    else
	scp ${TMPFILE} ${DSTDIR}
	mv ${TMPFILE} ${TMPFILE_PREV}
	SLEEP_SEC=10
    fi

    sleep ${SLEEP_SEC}
done

