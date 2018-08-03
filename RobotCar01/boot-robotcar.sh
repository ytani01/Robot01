#!/bin/sh

WORKDIR=${HOME}/Robot01/RobotCar01

cd ${WORKDIR}
. ./activate
./RobotCarServer.py 2>&1 &
../robot-http-server.sh 2>&1 &
