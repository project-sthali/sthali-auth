#!/bin/bash

set -e

if [ "$ENV" = 'DOCKER' ]; then
    echo "Running docker"
    exec docker run --name sthali-auth --rm -p 8000:80 sthali-auth
elif [ "$ENV" = 'LOCAL' ]; then
    echo "Running local"
    cd ./src/
    exec uvicorn run:app --host 0.0.0.0 --port 8002 --reload
else
    echo "No ENV found, nothing to run!!!"
fi
