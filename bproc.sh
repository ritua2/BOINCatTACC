#!/bin/bash

# File designed to keep the program running 
# Does the following in the following order
#    | 1) Reads the submitted files
#    | 2) Passes the commands to the BOINC server
#    | 3) Waits for 2.5 seconds to let OS clear memory
#    | 4) Sends the emails every 30 minutes

# Designed to be continously running using nohup#!/bin/bash

# Initiates the cron job for emails
crontab -l | { cat; echo "0,30 * * * * /root/project/email_assimilator.py"; } | crontab -
crontab -l | { cat; echo "0,30 * * * * /root/project/api/harbour.py"; } | crontab -

while true
do

   python3 /root/project/html/user/token_data/redfile.py
   python3 /root/project/html/user/token_data/red_runner.py
   sleep 3

done
