#!/bin/bash
gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:$PORT main:app