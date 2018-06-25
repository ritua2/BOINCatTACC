#!/bin/bash

# Designed for convenience in development
# This file is expected to be merged with advance-submit.sh



printf "Welcome to Boinc job submission\n\n"
printf "NOTE: NO MPI Jobs,No GPU, No jobs with external communication or large data transfer.\n"
# Server IP or domain must be declared before
SERVER_IP= # Declare it the first time this program is run


# Colors, helpful for printing
REDRED='\033[0;31m'
GREENGREEN='\033[0;32m'
YELLOWYELLOW='\033[1;33m'
NCNC='\033[0m' # No color


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



# All the allowed applications
# Each application contains: app=[image:version]
declare -A dockapps
dockapps=( ["autodock-vina"]="carlosred/autodock-vina:latest" ["bedtools"]="carlosred/bedtools:latest" ["blast"]="carlosred/blast:latest"
           ["bowtie"]="carlosred/bowtie:built" ["gromacs"]="carlosred/gromacs:latest"
           ["htseq"]="carlosred/htseq:latest" ["mpi-lammps"]="carlosred/mpi-lammps:latest" ["namd"]="carlosred/namd:latest")

numdocks=(1 2 3 4 5 6 7 8)




printf "Enter your selected option: "
read user_option

case "$user_option" in 

    "1")
        printf "\nSubmitting a file for a known dockerhub image with commands present\n"
        printf "\n${YELLOWYELLOW}WARNING${NCNC}\nAll commands must be entered, including results retrieval"
        printf "\nEnter the path of the file which contains list of serial commands: "
        read filetosubmit

        if [ ! -f $filetosubmit ]; then
            printf "File does not exist, program exited\n"
            exit 0
        fi

        curl -F file=@$filetosubmit http://$SERVER_IP:5075/boincserver/v2/submit_known/token=$TOKEN
        printf "\n"
        ;;

    "2")
        printf "\nSubmitting a BOINC job to a known image, select the image below:\n"

        # All the options
        printf "  1 Autodock-vina\n  2 Bedtools\n  3 Blast\n  4 Bowtie\n  5 Gromacs\n  6 HTSeq\n  7 MPI-LAMMPS\n  8 NAMD\n"
        printf "Enter option number: "
        read option2

        # Checks if the user has inputted a wrong option
        if [[ ${numdocks[*]} != *$option2* ]]; then
            printf "${REDRED}Application is not accepted\n${NCNC}Program exited\n"
            exit 0
        fi

        
        ;;

    *)
        printf "${REDRED}Invalid answer, program exited${NCNC}\n"
        exit 0


esac

