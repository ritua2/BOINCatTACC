#!/bin/bash

# Designed for convenience in development
# This file is expected to be merged with advance-submit.sh



printf "Welcome to Boinc job submission\n\n"
printf "NOTE: NO MPI Jobs,No GPU, No jobs with external communication or large data transfer.\n"
# Server IP or domain must be declared before
SERVER_IP=USER_SETUP # Declare it the first time this program is run


# Colors, helpful for printing
REDRED='\033[0;31m'
GREENGREEN='\033[0;32m'
NCNC='\033[0m' # No color

printf "$filetosubmit"
printf "Enter researcher email (must be registered first): "
read userEmail

# Validates the researcher's email against the server's API
TOKEN=$(curl -s -F email=$userEmail http://$SERVER_IP:5054/boincserver/v2/api/token_from_email)


# Checks that the token is valid
if [[ $TOKEN = *"INVALID"* ]]; then
    printf "${REDRED}User name is not valid or has not been registered\n${NCNC}Program exited\n"
    exit 0
fi

printf "${GREENGREEN}User verified with BOINC${NCNC}\n"


# Checks the user's allocation
allocation_check=$(curl -s -F token=$TOKEN http://$SERVER_IP:5052/boincserver/v2/api/simple_allocation_check)

if [ "$allocation_check" = 'n' ]; then
    printf "User allocation is insufficient, some options will no longer be allowed (${REDRED}red-colored${NCNC})\n"
fi


# Prints the text in color depending on the allocation status
alloc_color () {
    if [ "$allocation_check" = 'n' ]; then
        printf "${REDRED}$1${NCNC}\n"
    else
        printf "$1\n"
    fi
}


# Asks the user what they want to do
printf      "The allowed options are below:\n"
printf      "   1  Submitting a file with a list of commands from a dockerhub image (no extra files on this machine)\n"
alloc_color "   2  Submitting a BOINC job from a dockerhub image using local files in this machine"


printf "Enter your selected option: "
read user_option

case "$user_option" in 

    "1")
        printf "\nEnter the path of the file which contains list of serial commands: "
        read filetosubmit

        if [ ! -f $filetosubmit ]; then
            printf "File does not exist, program exited\n"
            exit 0
        fi

        curl -F file=@$filetosubmit http://$SERVER_IP:5075/boincserver/v2/submit_known/token=$TOKEN
        printf "\n"
        ;;

    *)
        printf "${REDRED}Invalid answer, program exited${NCNC}\n"
        exit 0


esac

