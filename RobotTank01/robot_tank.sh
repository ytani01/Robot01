#!/bin/sh

WORK_DIR=${HOME}/Robot01/RobotTank01

cd ${WORK_DIR}

. ./activate

exec ./robot_tank.py
