#!/bin/bash


# Generates a random identifier for the current server, a set of 32 random characters
export SERVER_ID=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)

# Adds the server as a mirror
curl -X POST -H "Content-Type: application/json" -d \
    '{"key":"'"$volcon_key"'", "disconnect-key":"'"$SERVER_ID"'"}' http://$main_server:5060/volcon/v2/api/mirrors/addme


# Activates the APIs (4 workers)
# Maximum timeout is 300 s
gunicorn -w 4 -b 0.0.0.0:7000 mirror:app --timeout 300
