#!bin/bash

############
# BASICS
#
# Necessary packages to set-up and work with a Redis database to store job submission
############

# Sets up a Redis client on port 6389

apt-get update -y
apt-get install redis-server git-core -y
git clone git://github.com/nrk/predis.git
mv predis/* ./user-interface/token_data
# Sets up a redis server on port 6389, which must be open in the docker-compose.yml
redis-server --port 6389 &
# Sets up python3, needed
apt-get install python3 python3-pip python3-mysql.connector -y
# Python modules
pip3 install redis Flask Werkzeug docker

# Moves all the APIs and email commands
# Requires to be cloned inside project
mv /root/project/boinc-updates/api /root/project
mv /root/project/boinc-updates/email_assimilator.py /root/project
mv /root/project/boinc-updates/user-interface/* /root/project/html/user
