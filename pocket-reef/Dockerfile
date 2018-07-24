##########################
# BASICS
# 
# An alpine server with python3 installed, useful only as a cloud storage server
# Not designed for front-end interfaces
#########################

FROM python:3.6-alpine


# Installs the necessary packages
# Bash for convenience
RUN apk update && apk add bash && mkdir -p /rdat && pip3 install Flask requests


# Server key, needed for connection
# Should be changed
ENV Reef_Key "Reef"

WORKDIR /rdat
