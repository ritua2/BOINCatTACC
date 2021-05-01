#!/bin/bash


# Starts or ends the Reef communication APIs


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

   nohup /reef/new_user.py & \
         > /dev/null 2>&1 & echo $! > /reef/nnuu_api.txt
   nohup /reef/reef_regular.py & \
        > /dev/null 2>&1 & echo $!  > /reef/rerg_api.txt
   nohup /reef/reef_results.py & \
        > /dev/null 2>&1 & echo $!  > /reef/rers_api.txt
   gunicorn -w 1 --certfile=certfile.crt --keyfile=keyfile.key -b 0.0.0.0:2003 new_node:app &

   printf "Reef APIs are now active\n"
fi


if [ $1 == "-down" ]; then 
   
   # Must compensate for the fork
   kill -9 $(($(cat /reef/nnuu_api.txt) - 1))
   kill -9 $(($(cat /reef/rerg_api.txt) - 1))
   kill -9 $(($(cat /reef/rers_api.txt) - 1))
   pkill gunicorn
   printf "Reef APIs have been disconnected\n"
fi
