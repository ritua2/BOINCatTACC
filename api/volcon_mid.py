#!/usr/bin/env python3


"""
BASICS

Connects and updates the list of VolCon instances and runners.
Does not receive results (volcon_results.py)
Does not process incoming jobs (volcon_jobs.py)
"""


import datetime
from flask import Flask, request, jsonify
import hashlib
import json
import mysql_interactions as mints
import redis


app = Flask(__name__)

r = redis.Redis(host = '0.0.0.0', port = 6389, db = 3)



# Checks a password withe respective type of Volcon system (mirrors)
def bad_password(volcon_type, given_password):

    try:
        system_key = r.hget(volcon_type, "Organization Token").decode("UTF-8")
        hp = hashlib.sha256(given_password.encode('UTF-8')).hexdigest()

        if hp == system_key:
            return False
        return True

    except:
        return True



# Given two lists, returns those values that are lacking in the second
# Empty if list 2 contains those elements
def l2_contains_l1(l1, l2):

    return[elem for elem in l1 if elem not in l2]



# Ensures that the server is VolCon available
@app.route("/volcon/v2/api/available")
def volcon_server():
    return "Server is VolCon able"



# Adds a VolCon mirror
# Each VolCon mirror is saved as a hash by the name M-{IP}, it is also provided as a key pair M-{IP}:"Organization Token" inside VolCon
# This key can be used in the future if an administrator wishes to disconnect any VolCon client from the system
# Requires a json input
@app.route('/volcon/v2/api/mirrors/addme', methods=['POST'])
def addme():

    # Ensures that there is an appropriate json request
    if not request.is_json:
        return "INVALID: Request is not json"

    proposal = request.get_json()

    # Checks the required fields
    req_fields = ["key", "disconnect-key"]
    req_check = l2_contains_l1(req_fields, proposal.keys())

    if req_check != []:
        return "INVALID: Lacking the following json fields to be read: "+",".join([str(a) for a in req_check])

    if bad_password("VolCon", proposal["key"]):
        return "INVALID: incorrect password"

    IP = request.environ['REMOTE_ADDR']

    if r.hexists("VolCon", "M-"+IP):
        return "INVALID: Server IP has already been assigned"

    V = {"IP":IP,
        "disconnect-key": proposal["disconnect-key"],
        "Jobs-Processed":"0",
        "Jobs in progress":"0"
    }

    r.hmset("M-"+IP, V)
    r.hset("VolCon", "M-"+IP, proposal["disconnect-key"])
    r.hincrby("VolCon", "Available-Mirrors", 1)

    return "Successfully added to the list of mirrors"



# Adds a VolCon client
# Each VolCon client is saved as a hash by the name cluster-{IP}, it is also provided as a key pair cluster-{IP}:"Organization Token" inside the cluster hash
# This key can be used in the future if an administrator wishes to disconnect any VolCon client from the system
# Requires a json input
@app.route('/volcon/v2/api/cluster/client/addme', methods=['POST'])
def client_addme():

    # Ensures that there is an appropriate json request
    if not request.is_json:
        return "INVALID: Request is not json"

    proposal = request.get_json()

    # Checks the required fields
    req_fields = ["cluster", "cluster-key", "disconnect-key"]
    req_check = l2_contains_l1(req_fields, proposal.keys())

    if req_check != []:
        return "INVALID: Lacking the following json fields to be read: "+",".join([str(a) for a in req_check])

    cluster = proposal["cluster"]
    if bad_password(cluster, proposal["cluster-key"]):
        return "INVALID: incorrect password"

    IP = request.environ['REMOTE_ADDR']

    if r.hexists(cluster, cluster+"-"+IP):
        return "INVALID: Server IP has already been assigned"

    V = {"IP":IP,
        "disconnect-key": proposal["disconnect-key"]
    }

    r.hmset(cluster+"-"+IP, V)
    r.hset(cluster, cluster+"-"+IP, proposal["disconnect-key"])

    return "Successfully added to the list of clients for the "+cluster+ " cluster"



# Updates the status of a job that is being run right now
@app.route('/volcon/v2/api/mirrors/status/update', methods=['POST'])
def status_update():

    # Ensures that there is an appropriate json request
    if not request.is_json:
        return "INVALID: Request is not json"

    proposal = request.get_json()

    # Checks the required fields
    req_fields = ["key", "VolCon-ID", "status"]
    req_check = l2_contains_l1(req_fields, proposal.keys())

    if req_check != []:
        return "INVALID: Lacking the following json fields to be read: "+",".join([str(a) for a in req_check])    

    if bad_password("VolCon", proposal["key"]):
        return "INVALID: incorrect password"

    try:
        mints.update_job_status(proposal["VolCon-ID"], proposal["status"], True)
        return "Successfully updated job "+ proposal["VolCon-ID"]
    except:
        return "Failed to update job"





if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5089, debug=False, threaded=True)

