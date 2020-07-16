#! /usr/bin/dumb-init /usr/bin/bash

echo ".......... STARTING CONTROLLER .........."
gunicorn -c gunicorn.conf manage:app