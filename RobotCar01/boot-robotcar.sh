#!/bin/sh

WORKDIR=${HOME}/Robot01/RobotCar01

${HOME}/bin/scp_ipaddr.sh &

cd ${WORKDIR}
. ./activate
./robot_tcpserver.py &
./robot_httpserver.py &
