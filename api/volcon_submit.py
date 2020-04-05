#!/usr/bin/env python3

"""
BASICS

Receives VolCon jobs from Stampede2/Lonestar5
"""



import datetime
from flask import Flask, request, jsonify
import hashlib
import json
import os
import random
import redis
import uuid

import mirror_interactions as mirror
import mysql_interactions as mints
import preprocessing as pp





app = Flask(__name__)
r = redis.Redis(host = '0.0.0.0', port = 6389, db = 3)


# Checks a password with the respective type of Volcon system (mirrors)
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



# Processes incoming jobs for TACC images
# Automatically assigns them to a mirror after the user receives the job
@app.route('/volcon/v2/api/jobs/tacc', methods=['POST'])
def tacc_jobs():

    # Ensures that there is an appropriate json request
    if not request.is_json:
        return "INVALID: Request is not json"

    proposal = request.get_json()

    if pp.token_test(proposal["token"]) == False:
       return 'Invalid token'

    # Checks the required fields
    req_fields = ["token", "image", "commands", "priority"]
    req_check = l2_contains_l1(req_fields, proposal.keys())

    if req_check != []:
        return "INVALID: Lacking the following json fields to be read: "+",".join([str(a) for a in req_check])    

    [TOKEN, IMAGE, COMMANDS, PRIORITY] = [proposal["token"], proposal["image"], proposal["commands"], proposal["priority"]]
    VolCon_ID = uuid.uuid4().hex

    if "gpu" in IMAGE:
        GPU = 1
    else:
        GPU = 0

    try:
        mints.add_job(TOKEN, IMAGE, COMMANDS, GPU, VolCon_ID, PRIORITY)
    except:
        return "INVALID: Could not connect to MySQL database"

    # TACC: Image is a TACC image
    job_info = {"Image":IMAGE, "Command":COMMANDS, "TACC":1, "GPU":GPU, "VolCon_ID":VolCon_ID, "public":1}

    mirror.upload_job_to_mirror(job_info)

    return "Successfully submitted job"



if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5093, debug=False, threaded=True)
