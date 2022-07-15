#! /bin/bash

# Go to working directory
BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd ${BASEDIR}

# start task
/root/.local/bin/celery -A tasks worker --loglevel=info -P solo

# cd Redis
# redis-server.exe redis.windows.conf
# redis-cli.exe -h 127.0.0.1 -p 6379
#streamlit run app.py