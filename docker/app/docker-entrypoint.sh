#!/bin/bash

SCRIPT_PATH=$(readlink -f `dirname "${0}"`)
cd ${SCRIPT_PATH}

exec python3 -m myapp.executable.main
ret=$?
echo ${ret}
