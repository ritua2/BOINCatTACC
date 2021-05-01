#!/bin/bash

# Ensures that the filesystem exists

if [ -z "$FILESYSTEM" ]; then
    error_message="ERROR: Environmental variable 'FILESYSTEM' is empty or not declared"
    >&2 echo "$error_message"
    exit
fi

filesystem_exists=$(df -h | grep "$FILESYSTEM")

if [ -z "$filesystem_exists" ]; then
    error_message="ERROR: Filesystem identified by 'FILESYSTEM' does not exist"
    >&2 echo "$error_message"
    exit
fi

read -ra OS_filesystem_info <<<"$filesystem_exists"

if [ "${OS_filesystem_info[0]}" != "$FILESYSTEM" ]; then
    error_message="ERROR: Filesystem identified by 'FILESYSTEM' does not exist"
    >&2 echo "$error_message"
    exit
fi

# Checks that variable is a positive integer
if ! [[ "$MAX_STORAGE" =~ ^[0-9]+$ ]]; then
    error_message="ERROR: Maximum total storage, identified by the 'MAX_STORAGE' variable must be an integer"
    >&2 echo "$error_message"
    exit
fi

# Checks that variable is a positive integer
if ! [[ "$RESERVED_STORAGE" =~ ^[0-9]+$ ]]; then
    error_message="ERROR: Reserved storage, identified by the 'MAX_STORAGE' variable must be an integer"
    >&2 echo "$error_message"
    exit
fi

if [ "$RESERVED_STORAGE" -gt "$MAX_STORAGE" ]; then
    error_message="ERROR: Reserved storage can't be more than Maximum storage"
    >&2 echo "$error_message"
    exit
fi

# Ensures that the available space is equal or larger than the maximum possible
available_space="${OS_filesystem_info[3]}" 
l_str_available_space=${#available_space}
let l_str_available_space_minus_1=$l_str_available_space-1
available_space_number=${available_space:0:$l_str_available_space_minus_1}
available_space_letter="${available_space: -1}"

if [ $available_space_letter = "G" ]; then
    # Data is in KB, multiplied by 10^6
    multiplier=1000000
elif [ $available_space_letter = "M" ]; then
    # Data is in KB, multiplied by 10^3
    multiplier=1000
else
    error_message="ERROR: Not enough available space, no G or M at end of 'Avail' for filesystem when executing 'df -h'"
    >&2 echo "$error_message"
    exit
fi

let available_space_KB=${available_space_number%.*}*$multiplier

if [ "$available_space_KB" -lt "$MAX_STORAGE" ]; then
    error_message="ERROR: Not enough available space, available space is ""$available_space_KB"" KB, whereas the MAX_STORAGE requested is ""$MAX_STORAGE"" KB"
    >&2 echo "$error_message"
    exit
fi

printf "\nNo errors with environmental variables\n"

# database stores everything in bytes
ALLOWED_STORAGE="$(($MAX_STORAGE - $RESERVED_STORAGE))"
mul=1000
ALLOWED_STORAGE_BYTES="$(($ALLOWED_STORAGE * $mul))"

curl -X POST -H "Content-Type: application/json"\
    -d '{"MAX_STORAGE":"'"$ALLOWED_STORAGE_BYTES"'", "NODE_KEY":"'"$NODE_KEY"'"}' \
    --insecure https://"$URL_BASE":2003/reef/cluster/addme

# Waits indefinitely
sleep infinity


