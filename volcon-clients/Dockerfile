############
# BASICS
#
# Implements a VolCon client
#
############


FROM python:3.6-alpine

ENV GPU="0"
ENV np="4"
ENV only_public="0"


COPY runner.sh /client/runner
COPY runner.py /client/runner.py
COPY closer.py /client/closer.py


# Installs the necessary packages
# Bash, curl for convenience
RUN apk update && apk add bash curl docker &&\
    pip3 install docker Flask requests &&\
    chmod +x /client/runner && touch /client/disconnect.txt


WORKDIR /client


CMD ["./runner"]

