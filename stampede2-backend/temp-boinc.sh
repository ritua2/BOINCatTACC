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
BLUEBLUE='\033[1;34m'
NCNC='\033[0m' # No color


printf "Enter researcher email (must be registered first): "
read userEmail

# Validates the researcher's email against the server's API
TOKEN=$(curl -s -F email=$userEmail http://$SERVER_IP:5054/boincserver/v2/api/token_from_email)


# Checks that the token is valid
if [[ $TOKEN = *"INVALID"* || -z "$TOKEN" ]]; then
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
alloc_color "   3  Submitting a BOINC job from a set of commands, unknown image, local files"



# All the allowed applications
# Each application contains: app=[image:version]
declare -A dockapps
dockapps=( ["autodock-vina"]="carlosred/autodock-vina:latest" ["bedtools"]="carlosred/bedtools:latest" ["blast"]="carlosred/blast:latest"
           ["bowtie"]="carlosred/bowtie:built" ["gromacs"]="carlosred/gromacs:latest"
           ["htseq"]="carlosred/htseq:latest" ["mpi-lammps"]="carlosred/mpi-lammps:latest" ["namd"]="carlosred/namd-cpu:latest"
           ["opensees"]="carlosred/opensees:latest")

numdocks=(1 2 3 4 5 6 7 8 9)
docknum=( ["1"]="autodock-vina" ["2"]="bedtools" ["3"]="blast"
           ["4"]="bowtie" ["5"]="gromacs"
           ["6"]="htseq" ["7"]="mpi-lammps" ["8"]="namd"
           ["9"]="opensees")

# Extra commands before each app
dockcomm=( ["1"]="" ["2"]="" ["3"]=""
           ["4"]="" ["5"]="source /usr/local/gromacs/bin/GMXRC.bash; "
           ["6"]="" ["7"]="" ["8"]=""
           ["9"]="")

# Some images don't accept curl, so they will use wget
curl_or_wget=( ["1"]="curl -O" ["2"]="wget " ["3"]="wget " 
            ["4"]="curl -O " ["5"]="curl -O " ["6"]="curl -O " 
            ["7"]="curl -O " ["8"]="curl -O " ["9"]="curl -O ")


########################################
# MIDAS OPTIONS
########################################

allowed_OS=("Ubuntu_16.04")
allowed_languages=("c" "c++" "c++ cget " "python" "python3" "fortran" "r" "bash" "")
languages_with_libs=("python" "python3" "c++ cget")



printf "Enter your selected option: "
read user_option

case "$user_option" in 

    "1")
        printf "\nSubmitting a file for a known dockerhub image with commands present\n"
        printf "\n${YELLOWYELLOW}WARNING${NCNC}\nAll commands must be entered, including results retrieval"
        printf "\nEnter the path of the file which contains list of serial commands: "
        read filetosubmit

        if [ ! -f $filetosubmit ]; then
            printf "${REDRED}File $filetosubmit does not exist, program exited${NCNC}\n"
            exit 0
        fi

        printf "\n$TOKEN" >> $filetosubmit

        curl -F file=@$filetosubmit http://$SERVER_IP:5075/boincserver/v2/submit_known/token=$TOKEN
        printf "\n"
        ;;

    "2")
        printf "\nSubmitting a BOINC job to a known image, select the image below:\n"

        # All the options
        printf "  1 Autodock-vina\n  2 Bedtools\n  3 Blast\n  4 Bowtie\n  5 Gromacs\n  6 HTSeq\n  7 MPI-LAMMPS\n  8 NAMD\n  9 OpenSEES\n"
        printf "Enter option number: "
        read option2

        # Checks if the user has inputted a wrong option
        if [[ ${numdocks[*]} != *$option2* ]]; then
            printf "${REDRED}Application is not accepted\n${NCNC}Program exited\n"
            exit 0
        fi

        user_app=${dockapps[${docknum[$option2]}]}

        # Obtains the image and the base commands
        # Add the possible source (such as in gromacs at the start
        user_command="$user_app /bin/bash -c \"cd /data; POSCOM"
        user_command=${user_command/POSCOM/${dockcomm[$option2]}}


        printf "Enter the list of input files (space-separated):\n"
        read -a user_ff
        

        # Checks the file and uploads it ito Reef (after checking that all the files exist)
        for ff in "${user_ff[@]}"
        do
            if [ ! -f $ff ]; then
                printf "${REDRED}File $ff does not exist, program exited${NCNC}\n"
                exit 0
            fi

        done

        for ff in "${user_ff[@]}"
        do
            AA=$(curl -s -F file=@$ff http://$SERVER_IP:5060/boincserver/v2/upload_reef/token=$TOKEN)

            if [[ $AA = *"INVALID"* ]]; then
                printf "${REDRED}$AA\n${NCNC}Program exited\n"
                exit 0
            fi

            # Appends to the user commands list
            user_command="$user_command GET_FILE http://$SERVER_IP:5060/boincserver/v2/reef/$TOKEN/$ff;"

        done

        # Replaces them by curl or wget, depending on the image
        user_command=${user_command//GET_FILE/${curl_or_wget[$option2]}}

        printf "\n${GREENGREEN}Files succesfully uploaded to BOINC server${NCNC}\n"


        # Asks the user for the lists of commands
        printf "\nEnter the list of commands, one at a time, as you would in the program itself (empty command to end):\n"
        while true
        do
            read COM

            if [ -z "$COM" ]; then
                break
            fi

            user_command="$user_command $COM;"
        done


        user_command="$user_command python /Mov_Res.py\""
        # Appends the job to a file and submits it
        printf "$user_command\n\n$TOKEN" > BOINC_Proc_File.txt
        curl -F file=@BOINC_Proc_File.txt http://$SERVER_IP:5075/boincserver/v2/submit_known/token=$TOKEN
        rm BOINC_Proc_File.txt
        printf "\n"        
        ;;

    "3")

        # MIDAS Processing
        printf "\nMIDAS job submission\n"
        printf "${YELLOWYELLOW}WARNING${NCNC} MIDAS is designed for prototyping\n"
        printf "For large scale job submission, use options 1 and 2\n"
        printf "\n"
        printf "%0.s-" {1..20}
        printf "\nAllowed OS:\n${BLUEBLUE}${allowed_OS[*]}${NCNC}\n"
        printf "Allowed languages:\n${BLUEBLUE}"
        printf "   %s" "${allowed_languages[@]}"
        printf "${NCNC}\n* python refers to python 3, since python2 is not accepted for MIDAS use\n"
        printf "%0.s-" {1..20}


        # In case the suer provides their own README
        printf "\nAre you providing a pre-compiled tar file (including README.txt) for MIDAS use in this directory?[y/n]\n"
        read README_ready
        if [[ "${README_ready,,}" = "y" ]]; then

            # Simply uploads the compressed file to MIDAS
            printf "\nEnter the compressed MIDAS job file: "
            read completed_midas

            if [ ! -f $completed_midas ]; then
                printf "${REDRED}File $completed_midas does not exist, program exited${NCNC}\n"
                exit 0
            fi

            # Makes sure that there is a README

            if ! tar --list --verbose --file=$completed_midas | grep -q "README.txt"; then
                printf "${REDRED}Invalid tar file, README missing${NCNC}\nProgram exited${NCNC}\n"
                exit 0
            fi


            curl -F file=@$completed_midas  http://$SERVER_IP:5085/boincserver/v2/midas/token=$TOKEN
            printf "\n"
            exit 0
        fi


        printf "Enter OS:\n"
        read user_OS
        if [[ "${allowed_OS[*]}" != *"$user_OS"* ]]; then
            printf "${REDRED}OS $user_OS is not accepted\n${NCNC}Program exited\n"
            exit 0
        fi


        printf "[OS] $user_OS\n" > README.txt
        

        printf "Enter languages used (space-separated):\n"
        read -a user_langs

        for LLL in "${user_langs[@]}"
        do
            if [[ "${allowed_languages[*]}" != *"${LLL,,}"* ]]; then
                printf "${REDRED}Language $LLL is not accepted\n${NCNC}Program exited\n"
                exit 0
            fi
            printf "[LANGUAGE] $LLL\n" >> README.txt
        done

        # Language libraries, taking into account that the language accepts them
        printf "Libraries:\n\n"
        printf "As of now, only the following languages accept libraries:\n python(3)   c++ cget\n"
        printf "Leave empty and press enter to skip or exit this prompt:\n\n"
        while true
        do
            printf "Enter language: "
            read liblang

            if [ -z "$liblang" ]; then
                break
            fi

            if [[ "${user_langs[*]}" != *"${liblang,,}"* ]]; then
                printf "${REDRED}Language $liblang was not entered before\n${NCNC}Program exited\n"
                exit 0
            fi

            if [[ "${languages_with_libs[*]}" != *"${liblang,,}"* ]]; then
                printf "${REDRED}Language $liblang does not accept libraries${NCNC}\nProgram exited"
                exit 0
            fi

            printf "Enter library: "
            read LIB

            if [ -z "$LIB" ]; then
                printf "${YELLOWYELLOW}WARNING ${NCNC} No libraries provided for $liblang, language skipped\n"
                continue
            fi

            printf "[LIBRARY] $liblang: $LIB\n" >> README.txt



        done



        ;;

    *)
        printf "${REDRED}Invalid answer, program exited${NCNC}\n"
        exit 0


esac