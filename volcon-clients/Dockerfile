############
# BASICS
#
# Implements a VolCon mirror that can temporarily store job files for a particular job
#
############


FROM python:3.6-alpine

ENV GPU="0"


COPY runner.sh /client/runner
COPY runner.py /client/runner.py
COPY closer.py /client/closer.py


# Installs the necessary packages
# Bash, curl for convenience
RUN apk update && apk add bash curl docker &&\
    pip3 install docker Flask requests &&\
    chmod +x /client/runner && touch /client/disconnect.txt &&\
    apk add openrc --no-cache && rc-update add docker boot


WORKDIR /client


CMD ["./runner"]

