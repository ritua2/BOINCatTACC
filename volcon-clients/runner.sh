#!/bin/bash


# Generates a random identifier for the current terminal, a set of 32 random characters
export SERVER_ID=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)

# Adds the server as a mirror
curl -X POST -H "Content-Type: application/json" -d \
    '{"cluster":"'"$cluster"'", "cluster-key":"'"$cluster-key"'", "disconnect-key":"'"$SERVER_ID"'"}' http://$main_server:5089/volcon/v2/api/cluster/client/addme


# Runs the client to receive and execute VolCon jobs
