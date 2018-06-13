#!/bin/bash

# Sets up the email and password credentials for the BOINC server
# This file can only be run once
# After this, it is necessary to manually modify /root/.bashrc


printf "Establishes the Dockerhub login credentials\n"
printf "WARNING\nThis file can only be run once, after it, modify the values directly in /root/.bashrc\n"
printf "Leave empty for empty variable\n"

printf "Dockerhub account: "
read DOCKERHUB
printf "\nDockerhub password: "
read DOCKERHUB_PASSWORD

printf "\nexport DOCKERHUB=$DOCKERHUB\nexport DOCKERHUB_PASSWORD=$DOCKERHUB_PASSWORD\n" >> /root/.bashrc
export DOCKERHUB=$DOCKERHUB
export DOCKERHUB_PASSWORD=$DOCKERHUB_PASSWORD
printf "Your variables have now been set and are accessible from command line\n"
