#!/bin/sh

WORKDIR=${HOME}/Robot01/RobotCar01

cd ${WORKDIR}
. ./activate
./robot_tcpserver.py &
./robot_httpserver.py &
