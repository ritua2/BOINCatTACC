#!/bin/bash

# Runs the emails in a loop due to a problem with cron variables

while true
do
    /home/boincadm/project/email_assimilator.py
    sleep 1200

done
