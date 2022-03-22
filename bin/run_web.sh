#!/usr/bin/env bash

LOGGING_LEVEL="${LOGGING_LEVEL:DEBUG}"
sleep 10s # compensate delay of mysql container setup
# run latest migrations
#flask db migrate
# directories for logs
mkdir -p /app/data/logs/web/

# run web server
gunicorn --reload --access-logfile "-" --error-logfile "-" --log-level LOGGING_LEVEL --worker-class gevent --workers=3 --timeout 60 --bind 0.0.0.0:8081 app:app
