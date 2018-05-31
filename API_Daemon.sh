#!/bin/bash

#Starts both BOINC APIs as background jobs that stay connected after ssh signal is over


# Both starts and finishes the jobs depending on the command


if [ $# -eq 0 ]; then
   printf "No arguments provided, use -h flag for help\n"
   exit 1
fi


if [ $1 == "-h" ]; then
   printf "Automatic API daemon set-up\n"
   printf "Use flag -up to set-up the APIs\n"
   printf "Use flag -down to cancel the APIs\n"
   exit 1
fi


if [ $1 == "-up" ]; then 

   nohup /root/project/api/server_checks.py & \
         > /dev/null 2>&1 & echo $! > sscc_api.txt

   nohup /root/project/api/submit_known.py & \
        > /dev/null 2>&1 & echo $! > sskk_api.txt
   printf "Server communication APIs are now active\n"
fi


if [ $1 == "-down" ]; then 
   
   # Must compensate for the fork
   kill -9 $(($(cat sscc_api.txt) - 1))
   kill -9 $(($(cat sskk_api.txt) - 1))
   printf "Server communication APIs have been disconnected\n"
fi
