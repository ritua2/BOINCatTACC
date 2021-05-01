##########################
# BASICS
# 
# An alpine server with python3 installed, useful only as a cloud storage server
# Not designed for front-end interfaces
#########################

FROM python:3.8.2-buster

# Copies the necessary files
COPY base_functions.py 	/reef/base_functions.py
COPY reef_storage_node.py 	/reef/reef_storage_node.py
COPY API_Daemon.sh 	/reef/API_Daemon.sh
COPY setup.sh		/reef/setup.sh
COPY certfile.crt	/reef/certfile.crt
COPY keyfile.key	/reef/keyfile.key

# Individual key used to attach node or to give it instructions
ENV NODE_KEY "node1"
# Similar to that of the manager node
ENV URL_BASE "IP_ADDRESS_OF_REEF_SERVER"
# Similar to that of the manager node
ENV MYSQL_DATABASE "reef"
# Similar to that of the manager node
ENV MYSQL_USER "root"
# Similar to that of the manager node
ENV MYSQL_PASSWORD "password"
# Filesystem where all data will stored. For example: /dev/sda1
ENV FILESYSTEM "overlay"
# Maximum total storage allowed for users in KB, must be a positive integer
ENV MAX_STORAGE "1000000"
# Reserved space for compressed files while downloading
ENV RESERVED_STORAGE "0"
# number of threads to run
ENV greyfish_threads "8"

# Installs the necessary packages
# Bash for convenience
RUN mkdir -p /rdat/sandbox && pip3 install gunicorn Flask mysql-connector-python requests &&\
	chmod +x /reef/setup.sh /reef/reef_storage_node.py /reef/API_Daemon.sh

WORKDIR /rdat
CMD /reef/setup.sh
