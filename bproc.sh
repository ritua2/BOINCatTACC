#!/bin/bash

# File designed to keep the program running 
# Does the following in the following order
#    | 1) Reads the submitted files
#    | 2) Passes the commands to the BOINC server
#    | 3) Sends the necessary emails
#    | 4) Waits for 2.5 seconds to let OS clear memory

# Designed to be continously running using nohup#!/bin/bash


while true
do

   python3 /root/project/html/user/token_data/redfile.py
   python3 /root/project/html/user/token_data/red_runner.py
   /root/project/email_assimilator.py
   sleep 3
done
