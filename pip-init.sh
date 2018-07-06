#!/bin/sh
#
ENVDIR=${HOME}/env
ACTIVATE_CMD=${ENVDIR}/bin/activate
PIP_PKGS="setuptools wheel pigpio smbus2"

cd

if [ ! -f ${ACTIVATE_CMD} ]; then
  echo ${ACTIVATE_CMD}: not found
  exit 1
fi

. ${ACTIVATE_CMD}

python -V

pip install -U ${PIP_PKGS}
