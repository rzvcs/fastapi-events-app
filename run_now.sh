#!/bin/bash

empty_line () {
    echo ""
    echo ""
}

throw_error_if_any () {
    ret=$?
    if [ $ret -ne 0 ]; then
        echo "[ERROR]: ret ${ret}"
        exit $ret
    fi
}

echo "[INFO]: Building docker image (quietly)"
docker build -q -t myapp:0.0.1 -f ./docker/app/Dockerfile .
throw_error_if_any
empty_line

echo "[INFO]: Building python virtual environment (quietly)"
python3 -m venv venv
throw_error_if_any

source venv/bin/activate
throw_error_if_any
pip install -r requirements-all.txt --quiet
throw_error_if_any
empty_line

echo "[INFO]: Running pytest and output coverage"
pytest --cov-report term --cov=myapp myapp/tests/
throw_error_if_any
empty_line

echo "[INFO]: Running docker app - use http://localhost:8080/docs to connect"
docker run -it --rm -p 8080:8080 myapp:0.0.1
throw_error_if_any
