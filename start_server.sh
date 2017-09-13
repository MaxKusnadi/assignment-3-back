#!/usr/bin/env bash
git pull
kill $(ps aux | grep 'assignment-3' | awk '{print $2}')
nohup gunicorn --certfile cert.pem --keyfile key.pem -k gevent -b 0.0.0.0:3000 --worker-connections 10 wsgi:app &
