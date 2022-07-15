FROM idas.chinaeast.cloudapp.chinacloudapi.cn/cbb/automl-api:base

ADD . .

RUN rm -fr run.py .git .gitignore *.md Dockerfile* deploy.sh jenkins.sh requirements.txt test whls \
    && rm -f /usr/local/include/python3.6m/opcode.h \
    && mkdir logs \
    && python3 -m compileall -b . \
    && find /usr/src/app -depth \
    \( \
        \( -type f -a \( -name '*.py' \) \) \
    \) -exec rm -rf '{}' +;

CMD [ "bash", "-x", "startup.sh" ]
