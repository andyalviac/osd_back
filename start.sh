#!/bin/bash
set -e
gunicorn -w 1 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:5000 app:app --reload &
nginx -g "daemon off;"
