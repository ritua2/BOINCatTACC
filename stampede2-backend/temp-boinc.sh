#!/bin/bash

# Designed for convenience in development
# This file is expected to be merged with advance-submit.sh



printf "Welcome to Boinc job submission\n\n"
printf "NOTE: NO MPI jobs distributed accross more than one volunteer, No jobs with external downloads while the job is running (no curl, wget, rsync, ..).\n"
# Server IP or domain must be declared before
SERVER_IP='boinc.tacc.utexas.edu'

# Colors, helpful for printing
REDRED='\033[0;31m'
GREENGREEN='\033[0;32m'
YELLOWYELLOW='\033[1;33m'
BLUEBLUE='\033[1;34m'
PURPLEPURPLE='\033[1;35m'
NCNC='\033[0m' # No color


printf "Enter email to which send results: "
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
TOKEN=$(curl -s -F email=$userEmail -F org_key=$ORK http://$SERVER_IP:5054/boincserver/v2/api/authorize_from_org)

# Checks that the token is valid
if [[ $TOKEN = *"INVALID"* ]]; then
    printf "${REDRED}Organization does not have access to BOINC\n${NCNC}Program exited\n"
    exit 0
fi

# Adds the username to the database if necessary
# Gets the actual user name
IFS='/' read -ra unam <<< "$PWD"
unam="${unam[3]}"

# Adds the username to the database if necessary
# Adds the username to the database if necessary
registerUser=$(curl -s http://$SERVER_IP:5078/boincserver/v2/api/add_username/$unam/$userEmail/$TOKEN/$ORK)

printf "\n${GREENGREEN}$registerUser${NCNC}\n"

printf "${GREENGREEN}BOINC connection established${NCNC}\n"


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


# Joins an array (str) into a joint string witha custom separator
function join_by {
    local IFS="$1"
    shift
    printf "$*"
}


# Asks the user what they want to do
printf      "The allowed options are below:\n"
alloc_color "   1  Submitting a BOINC job from TACC supported docker images using local files in this machine"
printf      "   2  Submitting a file with a list of commands from an existing dockerhub image (no extra files on this machine)\n"
alloc_color "   3  Submitting a BOINC job from a set of commands (source code, input local files) (MIDAS)"



# All the allowed applications
# Each application contains: app=[image:version]
declare -A dockapps
dockapps=( ["autodock-vina"]="carlosred/autodock-vina:latest" ["bedtools"]="carlosred/bedtools:latest" ["blast"]="carlosred/blast:latest"
           ["bowtie"]="carlosred/bowtie:built" ["gromacs"]="carlosred/gromacs:latest"
           ["htseq"]="carlosred/htseq:latest" ["mpi-lammps"]="carlosred/mpi-lammps:latest" ["namd"]="carlosred/namd-cpu:latest"
           ["opensees"]="saumyashah/opensees:latest" ["CUDA"]="carlosred/gpu:cuda" ["OpenFOAM6"]="carlosred/openfoam6:latest")

numdocks=(1 2 3 4 5 6 7 8 9 10 11)
docknum=( ["1"]="autodock-vina" ["2"]="bedtools" ["3"]="blast"
           ["4"]="bowtie" ["5"]="gromacs"
           ["6"]="htseq" ["7"]="mpi-lammps" ["8"]="namd"
           ["9"]="opensees" ["10"]="CUDA" ["11"]="OpenFOAM6")

# Extra commands before each app
dockcomm=( ["1"]="" ["2"]="" ["3"]=""
           ["4"]="" ["5"]="source /usr/local/gromacs/bin/GMXRC.bash "
           ["6"]="" ["7"]="" ["8"]=""
           ["9"]="" ["10"]="nvcc --version " ["11"]="source /opt/OpenFOAM/OpenFOAM-6/etc/bashrc ")

# Some images don't accept curl, so they will use wget
curl_or_wget=( ["1"]="curl -O" ["2"]="wget " ["3"]="wget " 
            ["4"]="curl -O " ["5"]="curl -O " ["6"]="curl -O " 
            ["7"]="curl -O " ["8"]="curl -O " ["9"]="curl -O " ["10"]="curl -O " ["11"]="curl -O ")

# Some images require the VolCon, whereas others do not
exwith=( ["1"]="boinc2docker" ["2"]="boinc2docker" ["3"]="boinc2docker"
           ["4"]="boinc2docker" ["5"]="boinc2docker"
           ["6"]="boinc2docker" ["7"]="boinc2docker" ["8"]="boinc2docker"
           ["9"]="boinc2docker" ["10"]="adtdp" ["11"]="boinc2docker")


# Tags for TACC-provided images
# Multiple subtopics split by ,
declare -A apptags
apptags=(  
                ["1"]="STEM"
                ["2"]="STEM"
                ["3"]="STEM"
                ["4"]="STEM"
                ["5"]="STEM"
                ["6"]="STEM"
                ["7"]="STEM"
                ["8"]="STEM"
                ["9"]="STEM"
                ["10"]="STEM"
                ["11"]="STEM")


########################################
# MIDAS OPTIONS
########################################

allowed_OS=("Ubuntu_16.04")
allowed_languages=("c" "c++" "python" "python3" "fortran" "r" "bash" )
languages_with_libs=("python" "python3" "c++")



printf "Enter your selected option: "
read user_option


case "$user_option" in 

    "1")
        printf "\nSubmitting a BOINC job to a known image, select the image below:\n"

        # All the options
        for key in "${!docknum[@]}"
        do
            printf "    $key) ${docknum[$key]}\n"
        done

        printf "Enter option number: "
        read option2

        # Checks if the user has inputted a wrong option
        if [[ ${numdocks[*]} != *$option2* ]]; then
            printf "${REDRED}Application is not accepted\n${NCNC}Program exited\n"
            exit 0
        fi

        user_app=${dockapps[${docknum[$option2]}]}
        boapp=${exwith[$option2]}

        # Tags are entered automatically
        chosen_tags=${apptags[$option2]}

        # Obtains the image and the base commands
        # Add the possible source (such as in gromacs at the start
        user_command="$user_app /bin/bash -c \"cd /data; "

        if [ ! -z "${dockcomm[$option2]}" ]; then
            user_command="$user_command ${dockcomm[$option2]} ; "
        fi


        printf "Enter the list of input files (space-separated):\n"
        read -a user_ff

        # Asks the user for directories
        printf "Enter list of local directories used (each in a new line, leave empty to exit):\n"
        printf "WARNING Local directories will maintain local structure in BOINC, user must take files out in a command if needed\n"
        UDIR=()
        while true
        do

            not_originally_here="False"
            read new_udir

            if [ -z "$new_udir" ]; then
                printf "No more directories have been added\n"
                break
            fi

            if [ ! -d "$new_udir" ]; then
                printf "${REDRED}$new_udir does not exist${NCNC}\nProgram exited\n"
                exit 0
            fi

            # If the directory is in a different location, it moves it to the present location and tars it
            if [ ! $(ls -d */ | grep "$new_udir") ]; then
                not_originally_here="True"
                cp -r "$new_udir" .
            fi

            # Changes the value of the file to delete the path in the name
            IFS='/' read -ra new_udir <<< "$new_udir"
            new_dir="${new_udir[-1]}"
            UDIR+=("$new_udir")

            tar -czf "$new_udir".tar.gz "$new_udir"

            # Removes local version of the repository, if it was not originally here
            if [ "$not_originally_here" = "True" ]; then
                rm -rf "$new_udir"
            fi

        done
        

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

        # Uploads the directories to Reef in their tar form
        for dirdir in "${UDIR[@]}"
        do
            Tarred_File="$dirdir".tar.gz
            AA=$(curl -s -F file=@$Tarred_File http://$SERVER_IP:5060/boincserver/v2/upload_reef/token=$TOKEN)

            if [[ $AA = *"INVALID"* ]]; then
                printf "${REDRED}$AA\n${NCNC}Program exited\n"
                exit 0
            fi

            # Adds directions to get the file and untar it
            user_command="$user_command GET_FILE http://$SERVER_IP:5060/boincserver/v2/reef/$TOKEN/$Tarred_File;"
            user_command="$user_command tar -xzf $Tarred_File;"

        done

        printf "\nUser files are being uploaded, do not press any keys ...\n"

        # Replaces them by curl or wget, depending on the image
        user_command=${user_command//GET_FILE/${curl_or_wget[$option2]}}

        printf "\n${GREENGREEN}Files succesfully uploaded to BOINC server${NCNC}\n"


        # If a user has multiple commands prepared, it submits those
        printf "Do you want to submit multiple commands for this application using an input file (one line per command) [y if yes]?: "
        read multiple_commands

        if [ "$multiple_commands" = "y" ]; then

            printf "\nEnter input file name: "
            read multicom_file

            if [ ! -f "$multicom_file" ]; then
                printf "${REDRED}File ""$multicom_file"" does not exist, program exited${NCNC}\n"
                exit 0
            fi

            cat "$multicom_file" | while read line
            do

                # Checks for empty lines
                if [ -z "$line" ]; then
                    continue
                fi

                # Checks for commands
                if [ $(echo "$line" | head -c 1) = "#" ]; then
                    continue
                fi

                previous_command="$user_command"

                # For all others, splits the command 
                IFS=';' read -r -a mcom <<< "$line"

                for COM in "${mcom[@]}"
                do
                    if [ -z "${dockcomm[$option2]}" ]; then
                        previous_command="$previous_command $COM;"
                        continue
                    fi

                    previous_command="$previous_command ${dockcomm[$option2]} && "
                    previous_command="$previous_command $COM;"
                done

                previous_command="$previous_command python /Mov_Res.py\""

                printf "$previous_command" > BOINC_Proc_File.txt

                cat BOINC_Proc_File.txt
                printf "\n"

                # Uploads the command to the server
                curl -F file=@BOINC_Proc_File.txt -F app=$boapp -F topics="$chosen_tags"  http://$SERVER_IP:5075/boincserver/v2/submit_known/token=$TOKEN/username=$unam
                rm BOINC_Proc_File.txt
                printf "\n"    

            done
            exit
        fi



        printf "\n\nSelected one job submission:\n\n"

        # Asks the user for the lists of commands
        printf "\nEnter the list of commands, one at a time, as you would in the program itself (empty command to end):\n"
        while true
        do
            read COM

            if [ -z "$COM" ]; then
                break
            fi

            if [ -z "${dockcomm[$option2]}" ]; then
                user_command="$user_command $COM;"
                continue
            fi

            user_command="$user_command ${dockcomm[$option2]} && "
            user_command="$user_command $COM;"
        done


        user_command="$user_command python /Mov_Res.py\""

        # Adds the commands to a text file to be submitted
        printf "$user_command" > BOINC_Proc_File.txt

        curl -F file=@BOINC_Proc_File.txt -F app=$boapp -F topics="$chosen_tags"  http://$SERVER_IP:5075/boincserver/v2/submit_known/token=$TOKEN/username=$unam
        rm BOINC_Proc_File.txt
        printf "\n"        
        ;;
        


    "2")
        printf "\nSubmitting a file for a known dockerhub image with commands present\n"
        printf "\n${YELLOWYELLOW}WARNING${NCNC}\nAll commands must be entered, including results retrieval"
        printf "\nEnter the path of the file which contains list of serial commands: "
        read filetosubmit


        if [ ! -f $filetosubmit ]; then
            printf "${REDRED}File $filetosubmit does not exist, program exited${NCNC}\n"
            exit 0
        fi

        # Read the file's first line and choose where the application
        # Same rule as before, if nvcc is present, then it is a GPU job
        boapp="boinc2docker"
        if cat $filetosubmit | grep "nvcc"; then
            boapp="adtdp"
        fi

        # Asks the user for topics
        chosen_tags=""

        printf "\nEnter a list of topics (separate by semicolons), leave empty to exit: "
        read chosen_tags


        curl -F file=@$filetosubmit -F app=$boapp -F topics="$chosen_tags" http://$SERVER_IP:5075/boincserver/v2/submit_known/token=$TOKEN/username=$unam
        printf "\n"
        ;;
        
    "3")

        # MIDAS Processing
        printf "\nMIDAS job submission\n"
        printf "${YELLOWYELLOW}WARNING${NCNC} MIDAS is designed for prototyping only, not for continuous job submission\n"
        printf "For large scale job submission, use options 1 and 2\n"
        printf "\n"
        printf "%0.s-" {1..20}
        printf "\nAllowed OS:\n${BLUEBLUE}${allowed_OS[*]}${NCNC}\n"
        printf "Allowed languages:\n${BLUEBLUE}"
        printf "   %s" "${allowed_languages[@]}"
        printf "${NCNC}\n* python refers to python 3, since python2 is not accepted for MIDAS use\n"
        printf "%0.s-" {1..20}

        boapp="boinc2docker"


        # In case the user provides their own README
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


            curl -F file=@$completed_midas -F app=$boapp  http://$SERVER_IP:5085/boincserver/v2/midas/token=$TOKEN/username=$unam
            printf "\n"
            exit 0
        fi


        printf "Enter ${PURPLEPURPLE}OS${NCNC}:\n"
        read user_OS

        for exOS in "${allowed_OS[@]}"
        do
            if [[ "$exOS" = *"$user_OS"* ]]; then
                used_OS="$exOS"
            fi
            break
        done


        if [ -z "$used_OS" ]; then
            printf "${REDRED}OS is invalid or not declared, program exited${NCNC}\n"
            exit 0
        fi


        printf "[OS] $used_OS\n" > README.txt
        

        printf "Enter ${PURPLEPURPLE}languages${NCNC} used (space-separated):\n"
        printf "If your command is within a bash file, enter all languages used within the bash file (i.e. if your bash file contains the instructions gcc hello.c -o h.out && ./a.out , select the languages bash c)"
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
        printf "\n${PURPLEPURPLE}Libraries${NCNC}\n"
        printf "As of now, only the following languages accept libraries:\n python(3)   c++ (using cget)\n"
        printf "Leave empty and press enter to skip or exit this prompt:\n\n"
        while true
        do
            printf "Enter language: "
            read liblang

            if [ -z "$liblang" ]; then
                break
            fi

            if [[ "${user_langs[*],,}" != *"${liblang,,}"* ]]; then
                printf "${REDRED}Language $liblang was not entered before\n${NCNC}Program exited\n"
                exit 0
            fi

            if [[ "${languages_with_libs[*]}" != *"${liblang,,}"* ]]; then
                printf "${REDRED}Language $liblang does not accept libraries${NCNC}\nProgram exited"
                exit 0
            fi

            if [ "${liblang,,}" = "c++" ]; then
                liblang="C++ cget"
            fi

            printf "Enter library  (one per line): "
            read LIB

            if [ -z "$LIB" ]; then
                printf "${YELLOWYELLOW}WARNING ${NCNC} No libraries provided for $liblang, language skipped\n"
                continue
            fi

            printf "[LIBRARY] $liblang: $LIB\n" >> README.txt

        done

        # Creates a new directory in which to temporarily put the files in
        rm -rf Temp-BOINC
        mkdir Temp-BOINC


        # Asks for user directories to be added to MIDAS
        # Asks the user for directories
        printf "\n\n\nEnter list of ${PURPLEPURPLE}local directories${NCNC} used (each in a new line, leave empty to exit):\n"
        printf "WARNING Local directories will maintain local structure in BOINC, MIDAs will automatically untar them\n"
        UDIR=()
        while true
        do

            read new_udir

            if [ -z "$new_udir" ]; then
                printf "No more directories have been added\n"
                break
            fi

            if [ ! -d "$new_udir" ]; then
                printf "${REDRED}$new_udir does not exist${NCNC}\nProgram exited\n"
                exit 0
            fi

            UDIR+=("$new_udir")

        done


        # Copies the directories to the inside of the MIDAS directory to be tarred
        # Adds a setup file to untar the directory
        for dirdir in "${UDIR[@]}"
        do
            cp -r "$dirdir" Temp-BOINC/
        done


        setfiles=()

        printf "\nEnter the ${PURPLEPURPLE}setup files${NCNC} (one per line), leave empty to exit:\n"
        while true
        do
            read setfil

            if [ -z "$setfil" ]; then
                break
            fi

            if [ ! -f $setfil ]; then
                printf "${REDRED}File $setfil does not exist, program exited${NCNC}\n"
                exit 0
            fi

            cp $setfil Temp-BOINC/

            setfiles+=("$setfil")
            printf "[USER_SETUP] $setfil\n" >> README.txt

        done


        comfiles=()
        printf "\n\nEnter the ${PURPLEPURPLE}commands${NCNC} below, leave empty to exit section:\n"
        printf "NOTE: If you wish to specify compilation and run instructions, please write them into a bash file, then select language bash, and provide the filename in the next prompt\n\n"


        while true
        do

            printf "Enter language: "
            read comlang

            if [ -z "$comlang" ]; then
                break
            fi

            if [[ "${user_langs[*],,}" != *"${comlang,,}"* ]]; then
                printf "${REDRED}Language $comlang was not entered before\n${NCNC}Program exited\n"
                exit 0
            fi

            printf "Enter file for command: "
            read comfil
            if [[ -z "$comfil" || ! -f $comfil ]]; then
                printf "${REDRED}File $comfil does not exist${NCNC}\n"
                continue
            fi

            cp $comfil Temp-BOINC/

            # Changes the value of the file to delete the path in the name
            IFS='/' read -ra comfil <<< "$comfil"
            comfil="${comfil[-1]}"


            # Languages C, C++, C++ CGET, and R require extra instructions

            case "${comlang,,}" in

                "r")
                    printf "Enter file to which write results (R only), leave empty to skip: "
                    read rwriter

                    if [ -z "$rwriter" ]; then
                        comfiles+=("$comlang: $comfil")
                    fi

                    comfiles+=("$comlang: $comfil: $rwriter")
                    ;;

                "c++")

                    printf "Answer the following questions, leave empty for None:\n"
                    ccom="$comlang: $comfil "

                    printf "Does it require CGET libraries?[y/n (empty is also no)]: "
                    read using_cget

                    if [ "${using_cget,,}" =  "y" ]; then

                        # Always uses adtd-p
                        boapp="adtdp"

                        ccom="$ccom: using CGET"

                        if ! cat README.txt |  grep -q 'LANGUAGE] C++ cget' ; then
                            printf "[LANGUAGE] C++ cget\n" >> README.txt
                        fi
                        printf "If these are the only libraries required, do not mention any more libraries in the section below\n"
                    fi

                    while true
                    do
                        printf "Enter any linked libraries (without -I flag): "
                        read newlib

                        if [ ! -z "$newlib" ]; then
                            ccom="$ccom: _1_ __I $newlib"
                        fi

                        printf "Enter any other flags or inputs (as is): "
                        read other_flags
                        if [ ! -z "$other_flags" ]; then
                            printf '2 for after file (i.e. gcc myfile -lgmp), any other for before: '
                            read flagorder

                            if [ "$flagorder" = "2" ]; then
                                ccom="$ccom: _2_ AS_IS $other_flags"
                            else
                                ccom="$ccom: _1_ AS_IS $other_flags"
                            fi
                        fi


                        printf "Continue?[y/n (empty is also no)]: "
                        read quescon

                        if [[ -z "$quescon" || "${quescon,,}" = "n" ]]; then
                            break
                        fi
                    done
                    comfiles+=("$ccom")
                    ;;


                "c")
                    printf "Answer the following questions, leave empty for None:\n"
                    ccom="$comlang: $comfil "
                    while true
                    do
                        printf "Enter any linked libraries (without -I flag): "
                        read newlib

                        if [ ! -z "$newlib" ]; then
                            ccom="$ccom: _1_ __I $newlib"
                        fi

                        printf "Enter any other flags or inputs (as is): "
                        read other_flags
                        if [ ! -z "$other_flags" ]; then
                            printf '2 for after file (i.e. gcc myfile -lgmp), any other for before: '
                            read flagorder

                            if [ "$flagorder" = "2" ]; then
                                ccom="$ccom: _2_ AS_IS $other_flags"
                            else
                                ccom="$ccom: _1_ AS_IS $other_flags"
                            fi
                        fi

                        printf "Continue?[y/n (empty is also no)]: "
                        read quescon

                        if [[ -z "$quescon" || "${quescon,,}" = "n" ]]; then
                            break
                        fi
                    done
                    comfiles+=("$ccom")
                    ;;

                *) 
                    # All other languages
                    comfiles+=("$comlang: $comfil")

            esac
        done


        # MIDAS requires commands to run
        if [ -z "${comfiles[*]}" ]; then
            printf "${REDRED}No commands provided, program exited${NCNC}\n"
            exit 0
        fi

        # Adds the commands to the README
        for nvnv in "${comfiles[@]}"
        do
            printf "[COMMAND] $nvnv\n" >> README.txt
        done


        # Asks which ouput files will be required
        # Avoids empty outputs
        while true
        do
            printf "Enter ${PURPLEPURPLE}output files${NCNC} or ALL, leave empty to exit: "
            read outfil

            if [ -z "$outfil" ]; then
                break
            fi

            prevfil=outfil
            if [ $outfil = "ALL" ]; then
                printf "[OUTPUT] $outfil\n" >> README.txt
                break
            fi

            printf "[OUTPUT] $outfil\n" >> README.txt
        done


        if [ -z "$prevfil" ]; then
            printf "${REDRED}No outputs provided, program exited${NCNC}\n"
            exit 0
        fi

        cp README.txt Temp-BOINC/


        # Tars the files and uploads the result to BOINC
        cd Temp-BOINC/
        Tnam="$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 8 | head -n 1).tar.gz"
        tar -czf "$Tnam" .

        curl -F file=@$Tnam -F app=$boapp http://$SERVER_IP:5085/boincserver/v2/midas/token=$TOKEN/username=$unam
        printf "\n"
        cd ..

        ;;

    *)
        printf "${REDRED}Invalid answer, program exited${NCNC}\n"
        exit 0

esac
