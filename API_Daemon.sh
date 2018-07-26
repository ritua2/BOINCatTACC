#!/bin/bash


# Starts both BOINC APIs as background jobs that stay connected after ssh signal is over


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
         > /dev/null 2>&1 & echo $! > /root/project/sscc_api.txt

   nohup /root/project/api/submit_known.py & \
        > /dev/null 2>&1 & echo $! > /root/project/sskk_api.txt
   nohup /root/project/api/reef_storage.py & \
        > /dev/null 2>&1 & echo $! > /root/project/rrff_api.txt
   nohup /root/project/api/factor2.py & \
        > /dev/null 2>&1 & echo $! > /root/project/fac2_api.txt 
   nohup /root/project/api/MIDAS.py & \
        > /dev/null 2>&1 & echo $! > /root/project/midd_api.txt
   nohup /root/project/api/allocation.py & \
        > /dev/null 2>&1 & echo $! > /root/project/allo_api.txt
   nohup /root/project/api/personal_area.py & \
        > /dev/null 2>&1 & echo $! > /root/project/prar_api.txt
   nohup /root/project/api/adtdp_common.py & \
        > /dev/null 2>&1 & echo $! > /root/project/adtd_api.txt
   nohup /root/project/api/webin.py & \
        > /dev/null 2>&1 & echo $! > /root/project/webi_api.txt
   nohup /root/project/api/ualdap.py & \
        > /dev/null 2>&1 & echo $! > /root/project/ldap_api.txt 
   nohup /root/project/api/t2auth.py & \
        > /dev/null 2>&1 & echo $! > /root/project/t2au_api.txt 
   nohup /root/project/api/signup_email.py & \
        > /dev/null 2>&1 & echo $! > /root/project/suem_api.txt 

   printf "Server communication APIs are now active\n"
fi


if [ $1 == "-down" ]; then 
   
   # Must compensate for the fork
   kill -9 $(($(cat /root/project/sscc_api.txt) - 1))
   kill -9 $(($(cat /root/project/sskk_api.txt) - 1))
   kill -9 $(($(cat /root/project/rrff_api.txt) - 1))
   kill -9 $(($(cat /root/project/fac2_api.txt) - 1))
   kill -9 $(($(cat /root/project/midd_api.txt) - 1))
   kill -9 $(($(cat /root/project/allo_api.txt) - 1))
   kill -9 $(($(cat /root/project/prar_api.txt) - 1))
   kill -9 $(($(cat /root/project/adtd_api.txt) - 1))
   kill -9 $(($(cat /root/project/webi_api.txt) - 1))
   kill -9 $(($(cat /root/project/ldap_api.txt) - 1))
   kill -9 $(($(cat /root/project/t2au_api.txt) - 1))
   kill -9 $(($(cat /root/project/suem_api.txt) - 1))
   printf "Server communication APIs have been disconnected\n"
fi
