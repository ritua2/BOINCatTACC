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
cp predis/* ./user-interface/token_data
# Sets up a redis server on port 6389, which must be open in the docker-compose.yml
redis-server --port 6389 &
# Sets up python3, needed
apt-get install python3 python3-pip python3-mysql.connector python3-ipy mailutils -y
# Python modules
pip3 install redis Flask Werkzeug captcha docker ldap3 requests pytz


# Changes all instances of http:// into https://


# Moves all the APIs and email commands
# Requires to be cloned inside project
cp -r ./api /home/boincadm/project
cp -r ./VM /home/boincadm/project
cp /home/boincadm/project/api/email_common.py /home/boincadm/project/VM
cp -r ./volcon /home/boincadm/project
cp ./email_assimilator.py /home/boincadm/project
cp ./email2.py /home/boincadm/project
cp ./email_all.py /home/boincadm/project
cp -r ./user-interface/* /home/boincadm/project/html/user
cp ./API_Daemon.sh  /home/boincadm/project
cp ./bproc.sh  /home/boincadm/project
cp ./password_credentials.sh /home/boincadm/project
cp ./dockerhub_credentials.sh /home/boincadm/project
cp ./idir.py /home/boincadm/project
cp ./boinc2docker_runner.py /home/boincadm/project/boinc2docker_runner.py
cp ./automail.sh /home/boincadm/project
mkdir /home/boincadm/project/adtd-protocol/process_files
mkdir /home/boincadm/project/adtd-protocol/tasks
mkdir /results/volcon

# Updates statistics
mv statistics_updater.py /home/boincadm/project/statistics_updater.py
chmod +x /home/boincadm/project/statistics_updater.py

# Moves the front end files
mv /home/boincadm/project/html/user /home/boincadm/project/html/user_old
cp -r ./user /home/boincadm/project/html/user
cp -r ./user/img1 /home/boincadm/project/html/user/


# Also moves the schedules
mv /home/boincadm/project/html/user_old/schedulers.txt /home/boincadm/project/html/user/schedulers.txt

# Substitutes the project and inc files by their new equivalents
mv /home/boincadm/project/html/inc /home/boincadm/project/html/inc_previous
cp -r ./inc /home/boincadm/project/html/inc
mv /home/boincadm/project/html/project /home/boincadm/project/html/project_old
cp -r ./project /home/boincadm/project/html/project
mv /home/boincadm/project/html/user_profile /home/boincadm/project/html/user_profile_old
cp -r ./user_profile /home/boincadm/project/html/user_profile
mkdir /home/boincadm/project/html/user_profile/images


chmod +x /home/boincadm/project/email_assimilator.py
chmod +x /home/boincadm/project/api/server_checks.py
chmod +x /home/boincadm/project/api/submit_known.py
chmod +x /home/boincadm/project/api/reef_storage.py
chmod +x /home/boincadm/project/api/MIDAS.py
chmod +x /home/boincadm/project/api/webin.py
chmod +x /home/boincadm/project/API_Daemon.sh
chmod +x /home/boincadm/project/bproc.sh
chmod +x /home/boincadm/project/html/user/token_data/create_organization.py
chmod +x /home/boincadm/project/html/user/token_data/modify_org.py
chmod +x /home/boincadm/project/api/factor2.py
chmod +x /home/boincadm/project/api/harbour.py
chmod +x /home/boincadm/project/api/allocation.py
chmod +x /home/boincadm/project/api/ualdap.py
chmod +x /home/boincadm/project/api/t2auth.py
chmod +x /home/boincadm/project/api/captcha_generator.py
chmod +x /home/boincadm/project/idir.py
chmod +x /home/boincadm/project/api/personal_area.py
chmod +x /home/boincadm/project/api/envar.py
chmod +x /home/boincadm/project/adtd-protocol/redfile2.py
chmod +x /home/boincadm/project/adtd-protocol/red_runner2.py
chmod +x /home/boincadm/project/api/adtdp_common.py
chmod +x /home/boincadm/project/api/signup_email.py
chmod +x /home/boincadm/project/api/newfold.py
chmod +x /home/boincadm/project/api/midasweb.py
chmod +x /home/boincadm/project/api/volcon*
chmod +x /home/boincadm/project/email2.py
chmod +x /home/boincadm/project/automail.sh
chmod +x /home/boincadm/project/VM/send_emails.py
chmod +x /home/boincadm/project/VM/send_emails_with_attachments.py


# Removes main directory restrictions
sed -i "159i# This line has been commented" /etc/apache2/apache2.conf
sed -i "160i# Commented" /etc/apache2/apache2.conf
sed -i "161i# Commented" /etc/apache2/apache2.conf
sed -i "162i# Commented" /etc/apache2/apache2.conf
sed -i "163i# Commented" /etc/apache2/apache2.conf

# Updates the scheduler
printf "<!-- <scheduler>$URL_BASE/boincserver_cgi/cgi</scheduler> -->\n" > /home/boincadm/project/html/user/schedulers.txt
printf "<link rel=\"boinc_scheduler\" href=\"$URL_BASE/boincserver_cgi/cgi\">" >> /home/boincadm/project/html/user/schedulers.txt


# Adds a DocumentRoot to the approproate configuration file
sed -i "s@DocumentRoot.*@DocumentRoot /home/boincadm/project/html/user/\n@"  /etc/apache2/sites-enabled/000-default.conf

# Changes the master URL to just the root
sed -i "s@<master_url>.*</master_url>@<master_url>$URL_BASE/</master_url>@" /home/boincadm/project/config.xml

# Changes the DB ops for the new BOINC 4
cat /home/boincadm/project/html/inc_previous/db_ops.inc > /home/boincadm/project/html/inc/db_ops.inc

# Changes to mass emails
cat /home/boincadm/project/BOINCatTACC > /home/boincadm/project/html/ops/mass_email.php

# Fixes issue with results not being copied in the correct directory
chmod -R a+rwx /results
chown -R www-data /home/boincadm/project/html/user_profile/
chgrp -R www-data /home/boincadm/project/html/user_profile/
chmod a-r /home/boincadm/project/html/user_profile/
chmod a-r /home/boincadm/project/html/user_profile/images
chmod a-r /home/boincadm/project/html/user_profile/img1

# Transfers ownership of stats directory to BOINC
chown -R www-data /home/boincadm/project/html/user/stats/
chgrp -R www-data /home/boincadm/project/html/user/stats/

# Restarts apache
service apache2 restart


/home/boincadm/project/API_Daemon.sh -up
nohup /home/boincadm/project/bproc.sh &

# Runs the emails on a loop due to cron problems
nohup /home/boincadm/project/automail.sh &

#################################### STATISTICS HAVE BEEN TEMPORARILY DISCONTINUED
# Creates the Redis Tag database
#python3 create_tag_db.py
#sed -i "12iprint('This action will restart the tag database, if you wish to continue, comment this line'); sys.exit()" create_tag_db.py


# Creates the MySQL tables
python3 create_MySQL_tables.py


# Needed to avoid confusion
sleep 2
printf "\nSet-up completed, server is ready now\n"
