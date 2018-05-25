#!bin/bash

############
# BASICS
#
# Necessary packages to set-up and work with a Redis database to store job submission
############

# Sets up a Redis client on port 6389

apt-get update -y
apt-get install redis-server git-core -y
# Sets up a redis server on port 6389, which must be open in the docker-compose.yml
redis-server --port 6389 &
# Sets up python3, needed
apt-get install python3 python3-pip -y
# Python modules
pip3 install redis
