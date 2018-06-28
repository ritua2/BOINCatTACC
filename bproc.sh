#!/bin/bash

# File designed to keep the program running 
# Does the following in the following order
#    | 1) Reads the submitted files
#    | 2) Passes the commands to the BOINC server
#    | 3) Waits for 2.5 seconds to let OS clear memory
#    | 4) Sends the emails every 30 minutes

# Designed to be continously running using nohup#!/bin/bash
# Adds environmental variables to the crontab
crontab -l | { cat; echo "SERVER_IP=$SERVER_IP"; } | crontab -
crontab -l | { cat; echo "BOINC_EMAIL=$BOINC_EMAIL"; } | crontab -
crontab -l | { cat; echo "BOINC_EMAIL_PASSWORD=$BOINC_EMAIL_PASSWORD"; } | crontab -

# Initiates the cron job for emails
crontab -l | { cat; echo "0,30 * * * * /root/project/email_assimilator.py"; } | crontab -
# Automatic dockerfile creation
crontab -l | { cat; echo "*/15 * * * * /root/project/api/harbour.py"; } | crontab -
# Erases all unaccounted images and stopped containers
crontab -l | { cat; echo "*/15 * * * * docker ps -aq --no-trunc -f status=exited | xargs docker rm"; } | crontab -
crontab -l | { cat; echo "*/15 * * * * docker images -q --filter dangling=true | xargs docker rmi -f"; } | crontab -

while true
do

   python3 /root/project/html/user/token_data/redfile.py
   python3 /root/project/html/user/token_data/red_runner.py
   sleep 15

done
