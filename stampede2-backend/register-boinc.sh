#!/bin/bash


# Designed for convenience in development
# This file is expected to be merged with advance-submit.sh



printf "Welcome to Boinc registration\n\n"
printf "This script will automatically set up credentials for submitting BOINC jobs\n\n\n"
# Server IP or domain must be declared before
SERVER_IP=boinc.tacc.utexas.edu # Declare it the first time this program is run

# Colors, helpful for printing
NCNC='\033[0m' # No color
REDRED='\033[0;31m'
GREENGREEN='\033[0;32m'

printf "Enter the email id to which the results should be sent: "
read userEmail


if [[ -z "$userEmail" || "$userEmail" != *"@"*"."* ]]; then 
    printf "${REDRED}Invalid format, not an email\n${NCNC}Program exited\n"
    exit 0
fi

# Gets the account for the org
# Only TACC hosts are accepted
domain_name=$(dnsdomainname)

# Reverses it, picks the first 15 letters, reverses it to ensure a correct domain
dn=$(echo "$domain_name" | rev)
ORK=$(echo "${dn:0:15}" | rev)


# Validates the researcher's email against the server's API
# Adds the username to the database if necessary
# Gets the actual user name
IFS='/' read -ra unam <<< "$PWD"
unam="${unam[3]}"

TOKEN=$(curl -s -F email=$userEmail -F org_key=$ORK -F username="$unam" http://$SERVER_IP:5054/boincserver/v2/api/authorize_from_org)

# Checks that the token is valid
if [[ $TOKEN = *"INVALID"* ]]; then
    printf "${REDRED}Organization does not have access to BOINC\n${NCNC}Program exited\n"
    exit 0
fi

printf "${GREENGREEN}BOINC connection established${NCNC}\n"
