#!/bin/sh -x
#
ENVDIR=${HOME}/env
ACTIVATE_CMD=${ENVDIR}/bin/activate
<<<<<<< HEAD
PIP_PKGS="setuptools wheel pigpio smbus2 readchar"
=======
PIP_PKGS="setuptools wheel pigpio smbus2 flask"
>>>>>>> 39a863a3c36a19d908ac4cffb1a6914566b175a5

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
