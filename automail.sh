#!/bin/bash

# Runs the emails in a loop due to a problem with cron variables

while true
do
	/root/project/email_assimilator.py
	/root/project/email2.py
	sleep 1200

done
