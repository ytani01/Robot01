#!/bin/sh

WORKDIR=${HOME}/Robot01/RobotCar01

cd ${WORKDIR}
. ./activate
./RobotCarServer.py &
./robot_httpserver.py &
