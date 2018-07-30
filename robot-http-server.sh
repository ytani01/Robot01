#!/bin/sh

WORKDIR=${HOME}/Robot01

if [ ! -d ${WORKDIR} ]; then
    echo "${WORKDIR}: not found."
    exit 1
fi

cd ${WORKDIR}

. ./activate

CMD="./robot-http-server.py"
if [ ! -x ${CMD} ]; then
    echo "${CMD}: not executable."
    ecit 2
fi
exec ${CMD} $*
