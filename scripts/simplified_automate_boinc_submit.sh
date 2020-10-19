#!/bin/bash

# Colors, helpful for printing
REDRED='\033[0;31m'
GREENGREEN='\033[0;32m'
YELLOWYELLOW='\033[1;33m'
BLUEBLUE='\033[1;34m'
PURPLEPURPLE='\033[1;35m'
NCNC='\033[0m' # No color

NEWLINE=$'\n'



printf "Welcome to Boinc job submission\n\n"
printf "NOTE: NO MPI jobs distributed accross more than one volunteer, No jobs with external downloads while the job is running (no curl, wget, rsync, ..).\n"
# Server IP or domain must be declared before
SERVER_IP='boinc.tacc.utexas.edu'


#printf "Enter the email id to which the results should be sent: "
#read userEmail
userEmail="vinaresults@gmail.com"

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
#printf      "The allowed options are below:\n"
#alloc_color "   1  Submitting a BOINC job from TACC supported docker images using local files in this machine"
#printf      "   2  Submitting a file with a list of commands from an existing dockerhub image (no extra files on this machine)\n"
#alloc_color "   3  Submitting a BOINC job from a set of commands (source code, input local files) (MIDAS)"



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



#printf "\nSubmitting a BOINC job to a known image, select the image below:\n"

# All the options
#for key in "${!docknum[@]}"
#do
#    printf "    $key) ${docknum[$key]}\n"
#done

#printf "Enter option number: "
#read option2
option2=1

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


#printf "Enter the list of input files (space-separated):\n"
#read -a user_ff

user_ff=$1







# If a user has multiple commands prepared, it submits those
printf "Do you want to submit multiple commands for this application using an input file (one line per command) [y if yes]?: "
read multiple_commands

multiple_commands="y"

if [ "$multiple_commands" = "y" ]; then

    printf "\nEnter the commands file name: "
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

        previous_command="$previous_command mv ./* /root/shared/results\""

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
    only_the_filename=$(basename "$ff")
    user_command="$user_command GET_FILE http://$SERVER_IP:5060/boincserver/v2/reef/$TOKEN/""$only_the_filename"";"

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


user_command="$user_command mv ./* /root/shared/results\""

# Adds the commands to a text file to be submitted
printf "$user_command" > BOINC_Proc_File.txt

curl -F file=@BOINC_Proc_File.txt -F app=$boapp -F topics="$chosen_tags"  http://$SERVER_IP:5075/boincserver/v2/submit_known/token=$TOKEN/username=$unam
rm BOINC_Proc_File.txt
printf "\n"        
