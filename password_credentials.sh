#!/bin/bash

# Sets up the email and password credentials for the BOINC server
# This file can only be run once
# After this, it is necessary to manually modify /root/.bashrc


printf "Append the user email and password\n"
printf "WARNING\nThis file can only be run once, after it, modify the values directly in /root/.bashrc\n"
printf "Leave empty for empty variable\n"

printf "Enter server IP (without http or port): "
read SERVER_IP
printf "Enter MySQL password credentials (empty for no password): "
read MYSQL_UPASS

printf "\nEnter email address: "
read BOINC_EMAIL
printf "\nEnter email password: "
read BOINC_EMAIL_PASSWORD

printf "\nexport SERVER_IP=$SERVER_IP\nexport BOINC_EMAIL=$BOINC_EMAIL\nexport BOINC_EMAIL_PASSWORD=$BOINC_EMAIL_PASSWORD\n" >> /root/.bashrc
printf "\nexport MYSQL_UPASS=$MYSQL_UPASS\n" >> /root/.bashrc
export SERVER_IP=$SERVER_IP
export MYSQL_UPASS="$MYSQL_UPASS"
export BOINC_EMAIL=$BOINC_EMAIL
export BOINC_EMAIL_PASSWORD=$BOINC_EMAIL_PASSWORD
printf "Your variables have now been set and are accessible from command line\n"
