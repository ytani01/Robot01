#!/bin/sh

WORKDIR1=${HOME}/Robot01
WORKDIR2=${WORKDIR1}/RobotTank01

if [ ! -d ${WORKDIR} ]; then
    echo "${WORKDIR}: not found."
    exit 1
fi

cd ${WORKDIR1}

. ./activate

CMD="./robot-http-server.py"
if [ ! -x ${CMD} ]; then
    echo "${CMD}: not executable."
    exit 2
fi
echo "starting ${CMD} ..."
${CMD} &

sleep 10

cd ${WORKDIR2}

CMD="./RobotTankServer.py"
if [ ! -x ${CMD} ]; then
    echo "${CMD}: not executable."
    exit 3
fi
echo "starting ${CMD} ..."
${CMD} $* &
