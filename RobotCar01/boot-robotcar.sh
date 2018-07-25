#!/bin/sh

WORKDIR=${HOME}/Robot01/RobotCar01

cd ${WORKDIR}
. ./activate
./RobotServer.py &
./robot_httpserver.py &
