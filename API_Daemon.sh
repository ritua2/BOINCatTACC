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

   nohup /home/boincadm/project/api/server_checks.py & \
         > /dev/null 2>&1 & echo $! > /home/boincadm/project/sscc_api.txt

   nohup /home/boincadm/project/api/submit_known.py & \
        > /dev/null 2>&1 & echo $! > /home/boincadm/project/sskk_api.txt
   nohup /home/boincadm/project/api/reef_storage.py & \
        > /dev/null 2>&1 & echo $! > /home/boincadm/project/rrff_api.txt
   nohup /home/boincadm/project/api/factor2.py & \
        > /dev/null 2>&1 & echo $! > /home/boincadm/project/fac2_api.txt 
   nohup /home/boincadm/project/api/MIDAS.py & \
        > /dev/null 2>&1 & echo $! > /home/boincadm/project/midd_api.txt
   nohup /home/boincadm/project/api/allocation.py & \
        > /dev/null 2>&1 & echo $! > /home/boincadm/project/allo_api.txt
   nohup /home/boincadm/project/api/personal_area.py & \
        > /dev/null 2>&1 & echo $! > /home/boincadm/project/prar_api.txt
   nohup /home/boincadm/project/api/adtdp_common.py & \
        > /dev/null 2>&1 & echo $! > /home/boincadm/project/adtd_api.txt
   nohup /home/boincadm/project/api/webin.py & \
        > /dev/null 2>&1 & echo $! > /home/boincadm/project/webi_api.txt
   nohup /home/boincadm/project/api/ualdap.py & \
        > /dev/null 2>&1 & echo $! > /home/boincadm/project/ldap_api.txt 
   nohup /home/boincadm/project/api/t2auth.py & \
        > /dev/null 2>&1 & echo $! > /home/boincadm/project/t2au_api.txt 
   nohup /home/boincadm/project/api/signup_email.py & \
        > /dev/null 2>&1 & echo $! > /home/boincadm/project/suem_api.txt 
   nohup /home/boincadm/project/api/envar.py & \
        > /dev/null 2>&1 & echo $! > /home/boincadm/project/envv_api.txt 
   nohup /home/boincadm/project/api/newfold.py & \
        > /dev/null 2>&1 & echo $! > /home/boincadm/project/nnff_api.txt 
   nohup /home/boincadm/project/api/midasweb.py & \
        > /dev/null 2>&1 & echo $! > /home/boincadm/project/mmww_api.txt 
   nohup /home/boincadm/project/api/volcon_jobs.py & \
        > /dev/null 2>&1 & echo $! > /home/boincadm/project/volj_api.txt 
   nohup /home/boincadm/project/api/volcon_mid.py & \
        > /dev/null 2>&1 & echo $! > /home/boincadm/project/volm_api.txt
   nohup /home/boincadm/project/api/volcon_submit.py & \
        > /dev/null 2>&1 & echo $! > /home/boincadm/project/vols_api.txt 
   nohup /home/boincadm/project/api/captcha_generator.py & \
        > /dev/null 2>&1 & echo $! > /home/boincadm/project/capt_api.txt
   nohup /home/boincadm/project/VM/send_emails.py & \
	    > /dev/null 2>&1 & echo $! > /home/boincadm/project/semail_api.txt 
   nohup /home/boincadm/project/VM/send_emails_with_attachments.py & \
        > /dev/null 2>&1 & echo $! > /home/boincadm/project/sewa_api.txt

   printf "Server communication APIs are now active\n"
fi


if [ $1 == "-down" ]; then 
   
   # Must compensate for the fork
   kill -9 $(($(cat /home/boincadm/project/sscc_api.txt) - 1))
   kill -9 $(($(cat /home/boincadm/project/sskk_api.txt) - 1))
   kill -9 $(($(cat /home/boincadm/project/rrff_api.txt) - 1))
   kill -9 $(($(cat /home/boincadm/project/fac2_api.txt) - 1))
   kill -9 $(($(cat /home/boincadm/project/midd_api.txt) - 1))
   kill -9 $(($(cat /home/boincadm/project/allo_api.txt) - 1))
   kill -9 $(($(cat /home/boincadm/project/prar_api.txt) - 1))
   kill -9 $(($(cat /home/boincadm/project/adtd_api.txt) - 1))
   kill -9 $(($(cat /home/boincadm/project/webi_api.txt) - 1))
   kill -9 $(($(cat /home/boincadm/project/ldap_api.txt) - 1))
   kill -9 $(($(cat /home/boincadm/project/t2au_api.txt) - 1))
   kill -9 $(($(cat /home/boincadm/project/suem_api.txt) - 1))
   kill -9 $(($(cat /home/boincadm/project/envv_api.txt) - 1))
   kill -9 $(($(cat /home/boincadm/project/nnff_api.txt) - 1))
   kill -9 $(($(cat /home/boincadm/project/mmww_api.txt) - 1))
   kill -9 $(($(cat /home/boincadm/project/volj_api.txt) - 1))
   kill -9 $(($(cat /home/boincadm/project/volm_api.txt) - 1))
   kill -9 $(($(cat /home/boincadm/project/vols_api.txt) - 1))
   kill -9 $(($(cat /home/boincadm/project/capt_api.txt) - 1))
   kill -9 $(($(cat /home/boincadm/project/semail_api.txt) - 1))
   kill -9 $(($(cat /home/boincadm/project/sewa_api.txt) - 1))
   printf "Server communication APIs have been disconnected\n"
fi

