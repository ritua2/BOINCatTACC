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

#   nohup /reef/reef_storage_node.py & \
#         > /dev/null 2>&1 & echo $! > /reef/rest_api.txt
   gunicorn -w $greyfish_threads --certfile=certfile.crt --keyfile=keyfile.key --timeout 600 -b 0.0.0.0:3443 reef_storage_node:app &
   printf "Reef storage API is  now active\n"
fi


if [ $1 == "-down" ]; then 
   
   # Must compensate for the fork
#   kill -9 $(($(cat /reef/rest_api.txt) - 1))
   pkill gunicorn

   printf "Reef storage API have been disconnected\n"
fi
