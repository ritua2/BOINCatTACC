#!/bin/bash

# Sets up the email and password credentials for the BOINC server
# This file can only be run once
# After this, it is necessary to manually modify /root/.bashrc


printf "Append the user email and password\n"
printf "WARNING\nThis file can only be run once, after it, modify the values directly in /root/.bashrc\n"
printf "Leave empty for empty variable\n"

printf "Enter server IP (without http or port): "
read SERVER_IP
printf "Enter MySQL username: "
read MYSQL_USER
printf "Enter MySQL password credentials (empty for no password): "
read MYSQL_UPASS

printf "\nEnter email address: "
read BOINC_EMAIL
printf "\nEnter email password: "
read BOINC_EMAIL_PASSWORD


# External Reef requirements
printf "\nEnter external Reef server IP: "
read Reef_IP
printf "\nEnter Reef key: "
read Reef_Key

# Some functionalities are implemented different in production and development
printf "\nIs this system a development server[y/other for no]? "
read dev_yn


printf "\nexport SERVER_IP=$SERVER_IP\nexport BOINC_EMAIL=$BOINC_EMAIL\nexport BOINC_EMAIL_PASSWORD=$BOINC_EMAIL_PASSWORD\n" >> /home/boincadm/.bashrc
printf "\nexport MYSQL_USER=$MYSQL_USER\nexport MYSQL_UPASS=$MYSQL_UPASS\nexport Reef_IP=$Reef_IP\nexport Reef_Key=$Reef_Key\n" >> /home/boincadm/.bashrc
printf "\nexport dev_yn=$dev_yn\n" >> /home/boincadm/.bashrc
export SERVER_IP="$SERVER_IP"
export MYSQL_USER="$MYSQL_USER"
export MYSQL_UPASS="$MYSQL_UPASS"
export BOINC_EMAIL=$BOINC_EMAIL
export BOINC_EMAIL_PASSWORD="$BOINC_EMAIL_PASSWORD"
export Reef_IP="$Reef_IP"
export Reef_Key="$Reef_Key"
export dev_yn="$dev_yn"
printf "Your variables have now been set and are accessible from command line\n"
