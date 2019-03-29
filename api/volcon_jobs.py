#!/usr/bin/env python3

"""
BASICS

Processes job submissions from the BOINC server
"""



from flask import Flask, request
import hashlib
import json
import mirror_interactions as mirror
import mysql_interactions as mints
import queue
import uuid

Q1 = queue.Queue()

app = Flask(__name__)


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



# Processes incoming jobs for TACC images
# Automatically assigns them to a mirror after the user receives the job
@app.route('/volcon/v2/api/jobs/tacc', methods=['POST'])
def tacc_jobs():

    # Ensures that there is an appropriate json request
    if not request.is_json:
        return "INVALID: Request is not json"

    proposal = request.get_json()

    # Checks the required fields
    req_fields = ["token", "image", "commands"]
    req_check = l2_contains_l1(req_fields, proposal.keys())

    if req_check != []:
        return "INVALID: Lacking the following json fields to be read: "+",".join([str(a) for a in req_check])    

    [TOKEN, IMAGE, COMMANDS] = [proposal["token"], proposal["image"], proposal["commands"]]
    VolCon_ID = uuid.uuid4().hex

    if "gpu" in IMAGE:
        GPU = 1
    else:
        GPU = 0

    try:
        mints.add_job(TOKEN, IMAGE, COMMANDS, GPU, VolCon_ID)
    except:
        return "INVALID: Could not connect to MySQL database"

    # TACC: Image is a TACC image
    job_info = {"Image":IMAGE, "Command":COMMANDS, "TACC":1, "GPU":GPU, "VolCon_ID":VolCon_ID}

    mirror.upload_job_to_mirror(job_info)
    Q1.put(VolCon_ID)

    return "Successfully submitted job"



# Receives a job request
# Returns the VolCon ID and where it is stored
@app.route('/volcon/v2/api/jobs/request', methods=['POST'])
def request_job():

    if not request.is_json:
        return "INVALID: Request is not json"    

    # Checks the required fields
    req_fields = ["cluster", "GPU", "runner-id"]
    req_check = l2_contains_l1(req_fields, proposal.keys())

    if req_check != []:
        return "INVALID: Lacking the following json fields to be read: "+",".join([str(a) for a in req_check]) 


    # Ensures the VolCon runner is associated with a valid cluster
    # TODO


    # Checks the status of the queue for a new job
    if not Q1.empty():
        try:
            # 1 s to avoid race conditions
            VolCon_ID = Q1.get(timeout=1)
        except:
            return "No jobs available"
    else:
        return "No jobs available"


    # Finds the mirror location of the files
    return mints.get_mirror_for_job(VolCon_ID)






if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5091, debug=False, threaded=True)


