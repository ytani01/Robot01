#!/bin/sh -x
#
ENVDIR=${HOME}/env
ACTIVATE_CMD=${ENVDIR}/bin/activate
PIP_PKGS="setuptools wheel pigpio smbus2 readchar flask netifaces"

cd

if [ ! -f ${ACTIVATE_CMD} ]; then
  echo ${ACTIVATE_CMD}: not found
  exit 1
fi

set +x
. ${ACTIVATE_CMD}
set -x

python -V

pip install -U ${PIP_PKGS}
