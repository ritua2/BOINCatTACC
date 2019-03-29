############
# BASICS
#
# Implements a VolCon mirror that can temporarily store job files for a particular job
#
############


FROM python:3.6-alpine


COPY runner.sh /client/runner
COPY runner.py /client/runner.py


# Installs the necessary packages
# Bash, curl for convenience
RUN apk update && apk add bash curl &&\
    pip3 install gunicorn Flask requests &&\
    chmod +x /client/runner


WORKDIR /client


CMD ["./runner"]

