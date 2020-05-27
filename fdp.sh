#!/bin/bash

# host name and port
if [ ! $HOST_NAME ]; then
    HOST_NAME='0.0.0.0'
fi

if [ ! $HOST_PORT ]; then
    HOST_PORT=8080
fi

# SPARQL database endpoint
if [ ! $DB_ENDPOINT ]; then
    DB_ENDPOINT=None
else
    DB_ENDPOINT=\'${DB_ENDPOINT}\'
fi

echo ${HOST_NAME} ${HOST_PORT} ${DB_ENDPOINT}
python -m bottle --server='paste' --bind=${HOST_NAME}:${HOST_PORT} "fdp.fdp:run_app(host='${HOST_NAME}', port=${HOST_PORT}, endpoint=${DB_ENDPOINT})"