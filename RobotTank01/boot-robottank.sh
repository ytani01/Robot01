#!/bin/sh

WORKDIR=${HOME}/Robot01/RobotTank01

cd ${WORKDIR}
. ./activate
./RobotTankServer.py 2>&1 &
../robot-http-server.sh 2>&1 &
