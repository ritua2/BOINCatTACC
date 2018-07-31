#!bin/bash

############
# BASICS
#
# Necessary packages to set-up and work with a Redis database to store job submission
############


# Requirements
# |   Ubuntu system, preferably > 16
# |   Docker installed
# |   Internet connection

# Sets up a Redis client on port 6389

apt-get update -y
apt-get install redis-server vim git-core -y
git clone git://github.com/nrk/predis.git
mv predis/* ./user-interface/token_data
# Sets up a redis server on port 6389, which must be open in the docker-compose.yml
redis-server --port 6389 &
# Sets up python3, needed
apt-get install python3 python3-pip python3-mysql.connector -y
# Python modules
pip3 install redis Flask Werkzeug docker ldap3 requests

# Moves all the APIs and email commands
# Requires to be cloned inside project
mv ./api /root/projec
mv ./adtd-protocol /root/project
mv ./email_assimilator.py /root/project
mv ./email2.py /root/project
mv ./user-interface/* /root/project/html/user
mv ./API_Daemon.sh  /root/project
mv ./bproc.sh  /root/project
mv ./password_credentials.sh /root/project
mv ./dockerhub_credentials.sh /root/project
mv ./idir.py /root/project
mkdir /root/project/adtd-protocol/process_files
mkdir /root/project/adtd-protocol/tasks
mkdir /results/adtdp

# Moves the front end files
mv /root/project/html/user /root/project/html/user_old
#mv ./user/img1 /root/project/html/user/
mv ./user /root/project/html/user

# Also moves the schedules
mv /root/project/html/user_old/schedulers.txt /root/project/html/user/schedulers.txt

# Required because images is its own directory
#mv -f ./user/img/* /root/project/html/user/img

# Substitutes the project and inc files by their new equivalents
mv /root/project/html/inc /root/project/html/inc_previous
mv ./inc /root/project/html/inc
mv /root/project/html/project /root/project/html/project_old
mv ./project /root/project/html/project
mv /root/project/html/user_profile /root/project/html/user_profile_old
mv ./user_profile /root/project/html/user_profile


chmod +x /root/project/email_assimilator.py
chmod +x /root/project/api/server_checks.py
chmod +x /root/project/api/submit_known.py
chmod +x /root/project/api/reef_storage.py
chmod +x /root/project/api/MIDAS.py
chmod +x /root/project/api/webin.py
chmod +x /root/project/API_Daemon.sh
chmod +x /root/project/bproc.sh
chmod +x /root/project/html/user/token_data/create_organization.py
chmod +x /root/project/html/user/token_data/modify_org.py
chmod +x /root/project/api/factor2.py
chmod +x /root/project/api/harbour.py
chmod +x /root/project/api/allocation.py
chmod +x /root/project/api/ualdap.py
chmod +x /root/project/api/t2auth.py
chmod +x /root/project/idir.py
chmod +x /root/project/api/personal_area.py
chmod +x /root/project/api/envar.py
chmod +x /root/project/adtd-protocol/redfile2.py
chmod +x /root/project/adtd-protocol/red_runner2.py
chmod +x /root/project/api/adtdp_common.py
chmod +x /root/project/api/signup_email.py
chmod +x /root/project/email2.py


# Asks the user to make the main directory available
printf "Enter the apache2.conf and comment out the main directory restrictions\nThis message will stay for 20 s\n"
sleep 20
vi /etc/apache2/apache2.conf

printf "<link rel=\"boinc_scheduler\" href=\"$URL_BASE/boincserver_cgi/cgi\">" > /root/project/html/user/schedulers.txt


# Adds a DocumentRoot to the approproate configuration file
sed -i "s@DocumentRoot.*@DocumentRoot /root/project/html/user/\n@"  /etc/apache2/sites-enabled/000-default.conf

# Changes the master URL to just the root
sed -i "s@<master_url>.*</master_url>@<master_url>$URL_BASE/</master_url>@" /root/project/config.xml

# Restarts apache
service apache2 restart


/root/project/API_Daemon.sh -up
nohup /root/project/bproc.sh &

# Needed to avoid confusion
sleep 2
printf "\nSet-up completed, server is ready now\n"
