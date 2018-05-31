#!/bin/bash

#Starts both BOINC APIs as background jobs that stay connected after ssh signal is over


# Both starts and finishes the jobs depending on the command


if [ $# -eq 0 ]; then
   printf "No arguments provided, use -h flag for help\n"
   exit 1
fi

if [ $1 == "-h" ]; then
   printf "Automatic API daemon set-up\n"
   exit 1
fi


#nohup /root/project/api/server_checks.py &
#nohup /root/project/api/submit_known.py &

#printf "API communication is now active\n"
