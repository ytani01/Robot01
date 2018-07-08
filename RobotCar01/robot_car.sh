#!/bin/sh

WORK_DIR=${HOME}/Robot01/RobotCar01

cd ${WORK_DIR}

. ./activate

exec ./robot_car.py
