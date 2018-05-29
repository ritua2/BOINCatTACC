#!/bin/bash

echo "Welcome to Boinc job submission:"
echo "NOTE: NO MPI Jobs,No GPU, No jobs with external communication, large data transfer is expected."
echo -n "Enter the path of the file which contains list of serial commands : "
read filetosubmit
echo "$filetosubmit"
echo -n "Enter the your user tocken : "
read userTocken
echo -n "Enter the boinc server ip address : "
read SERVER_IP

curl -F file=@$filetosubmit http://$SERVER_IP:5075/boincserver/v2/submit_known/token=$userTocken
echo "Your request is submitted."
