#!/bin/sh

CONF_FILE=${HOME}/bin/conf.sh
CMD=robot1.py

if [ -f ${CONF_FILE} ]; then
	. ${CONF_FILE}
else
	echo "${CONF_FILE}: not found."
	exit 1
fi

if [ X${VIRTUAL_ENV} = X ]; then
	if [ -f ${ENVBIN}/activate ]; then
		. ${ENVBIN}/activate
	fi
fi
echo "VIRTUAL_ENV=${VIRTUAL_ENV}"
