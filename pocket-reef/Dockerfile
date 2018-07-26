##########################
# BASICS
# 
# An alpine server with python3 installed, useful only as a cloud storage server
# Not designed for front-end interfaces
#########################

FROM python:3.6-alpine


# Copies the necessary files
COPY base_functions.py /reef/base_functions.py
COPY new_user.py /reef/new_user.py
COPY reef_results.py /reef/reef_results.py
COPY reef_regular.py /reef/reef_regular.py
COPY API_Daemon.sh /reef/API_Daemon.sh


# Installs the necessary packages
# Bash for convenience
RUN apk update && apk add bash && mkdir -p /rdat && mkdir /rdat/sandbox && pip3 install Flask requests &&\
	chmod +x /reef/new_user.py /reef/reef_regular.py /reef/reef_results.py /reef/API_Daemon.sh


WORKDIR /rdat