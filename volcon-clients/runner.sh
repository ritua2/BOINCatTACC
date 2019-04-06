#!/bin/bash


# Generates a random identifier for the current server, a set of 32 random characters
export disconnect_key=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)

# Adds the server as a cluster
curl -X POST -H "Content-Type: application/json" -d \
    '{"cluster":"'"$cluster"'", "cluster-key":"'"$cluster_key"'", "disconnect-key":"'"$disconnect_key"'"}' \
    http://$main_server:5089/volcon/v2/api/cluster/client/addme


# By default, the system can execute all priorities
printf '{
    "available-priorities":["Urgent", "Middle", "Low"]


}' >> /client/priorities.json


# If anyone sends the disconnect key, it kills the container
wait_for_disconnect () {

    # Continuously checks the same file
    while true; do
        dk=$(cat /client/disconnect.txt)

        if [ "$dk" = "$disconnect_key" ]; then
            kill 1
        fi
    done

}


python3 /client/closer.py &
wait_for_disconnect &

# Runs the client to receive and execute VolCon jobs
python3 /client/runner.py
