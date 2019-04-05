#!/usr/bin/env python3

"""
BASICS

Processes job submissions from the BOINC server
"""



import datetime
import email_common as ec
from flask import Flask, request, jsonify
import hashlib
import json
import mirror_interactions as mirror
import mysql_interactions as mints
import os
import random
import redis
import requests
import uuid
from werkzeug.utils import secure_filename





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



def present_day():
    return datetime.datetime.utcnow().strftime("%Y-%m-%d")



# Currently, tokens are also emails
def email_from_token(token):
    return token


# Processes incoming jobs for TACC images
# Automatically assigns them to a mirror after the user receives the job
@app.route('/volcon/v2/api/jobs/tacc', methods=['POST'])
def tacc_jobs():

    # Ensures that there is an appropriate json request
    if not request.is_json:
        return "INVALID: Request is not json"

    proposal = request.get_json()

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
    job_info = {"Image":IMAGE, "Command":COMMANDS, "TACC":1, "GPU":GPU, "VolCon_ID":VolCon_ID}

    mirror.upload_job_to_mirror(job_info)
    # Adds tag
    mints.tag_volcon(VolCon_ID)

    return "Successfully submitted job"



# Receives a job request
# Returns the VolCon ID and where it is stored
@app.route('/volcon/v2/api/jobs/request', methods=['POST'])
def request_job():

    if not request.is_json:
        return "INVALID: Request is not json"    

    proposal = request.get_json()
    # Checks the required fields
    req_fields = ["cluster", "disconnect-key", "GPU", "priority-level"]
    req_check = l2_contains_l1(req_fields, proposal.keys())

    if req_check != []:
        return "INVALID: Lacking the following json fields to be read: "+",".join([str(a) for a in req_check])

    # By default, it assumes public jobs, change it to 0 to account for MIDAS
    wants_public_jobs = 1
    if "public" in proposal.keys():
        wants_public_jobs = proposal["public"]

    # Ensures the VolCon client is associated with a valid cluster
    IP = request.environ['REMOTE_ADDR']
    cluster = proposal["cluster"]
    if not r.hexists(cluster, cluster+"-"+IP):
        return "INVALID: Server IP is not associated with cluster ' "+cluster+ "'"
    # Ensures that the key provided for this particular server is correct
    if r.hget(cluster, cluster+"-"+IP).decode("UTF-8") != proposal["disconnect-key"]:
        return "INVALID key"

    # Obtains a list of valid volcon_IDs and their respective mirror IPs
    volmir = mints.available_jobs(proposal["GPU"], proposal["priority-level"], public=wants_public_jobs)
    random.shuffle(volmir)
    if volmir == []:
        return jsonify({"jobs-available":"0"})

    # Locks and selects the first one for execution to avoid race conditions
    unavailable = True

    for item in volmir:
        VID = item[0]
        new_status = "Job has been requested by client"
        if not mints.race_condition_occurred(VID):
            try:
                mints.update_job_status(VID, new_status, True)
            except:
                continue            
            VolCon_ID = VID
            mirror_IP = item[1]
            unavailable = False
            break

    if unavailable:
        return jsonify({"jobs-available":"0"})

    # Finds the mirror location of the files
    return jsonify({"VolCon-ID":VolCon_ID, "mirror-IP":mirror_IP})



# Receives job files
# Does NOT update the database, see next API
@app.route("/volcon/v2/api/jobs/results/upload/<VID>", methods=['POST'])
def results_upload(VID):

    prestime = mints.timnow()

    # Checks out if the given VolCon-ID exists in database
    if not mints.VolCon_ID_exists(VID):
        return "INVALID: VolCon-ID does not exist"

    try:
        file = request.files["file"]
    except:
        return "INVALID, file not provided"

    # Always in the same location
    location = "/results/volcon/"+present_day()

    # Creates directory if needed
    if present_day() not in os.listdir("/results/volcon"):
        # Creates directory, avoids race conditions
        try:
            os.mkdir(location)
        except:
            pass

    new_name = secure_filename(file.filename)
    # Saves the file
    file.save(location+"/"+new_name)

    # Updates the status in the database
    mints.update_job_status(VID, "Results received", False)

    return "Results uploaded"


# Receives job data, updates the database, sends researcher an email
@app.route('/volcon/v2/api/jobs/upload/report', methods=['POST'])
def upload_report():

    if not request.is_json:
        return "INVALID: Request is not json"    
    proposal = request.get_json()
    # Checks the required fields
    req_fields = ["date (Run)", "VolCon-ID", "download time", "Commands", "Result Error", "computation time"]
    req_check = l2_contains_l1(req_fields, proposal.keys())

    if req_check != []:
        return "INVALID: Lacking the following json fields to be read: "+",".join([str(a) for a in req_check])

    VolCon_ID = proposal["VolCon-ID"]
    if not mints.VolCon_ID_exists(VolCon_ID):
        return "INVALID: VolCon-ID does not exist"

    command_errors = proposal["Commands"][1]
    computation_time = proposal["computation time"]
    date_run = proposal["date (Run)"]
    download_time = proposal["download time"]
    received_time = mints.timnow()
    result_error = proposal["Result Error"]

    user_token = mints.token_from_VolCon_ID(VolCon_ID)
    researcher_email = email_from_token(user_token)

    Error = "" # By default

    if set(command_errors) != {"Success"}:
        Error = ",".join([str(x) for x, y in zip(range(0, len(command_errors)), command_errors) if y != "Success" ])

    if result_error != "0":
        Error += ";"+result_error
        # No attachments can be added since none where updated
        attachments = []
    else:
        # Finds the attachments, in chronological order starting at a date
        attachments = [ec.obtain_file_received_at_date(VolCon_ID+".tar", received_time)[0]]
        result_error = "No errors retrieving data"

    if Error == "":
        Error = None
        outcome = "Success"
        specific_command_errors = None
        # Uploads the data to Reef
        requests.post('http://'+os.environ['Reef_IP']+':2001/reef/result_upload/'+os.environ['Reef_Key']+'/'+user_token,
                    files={"file": open(attachments[0], "rb")})
    else:
        # Types of error
        outcome = "Computational error"
        attachments = []
        specific_command_errors = ",".join(command_errors)+";"+result_error

    # Sends email to user
    email_notification = ec.send_mail_complete(researcher_email, "BOINC job complete", ec.automatic_text(received_time, outcome, user_token, attachments),
                    attachments)

    client_IP = request.environ['REMOTE_ADDR']

    # Updates the database
    mints.update_execution_report(VolCon_ID, specific_command_errors, computation_time, date_run, download_time,
                                Error, email_notification, client_IP)

    return "Server has processed the results"



# Receives failed job notification
@app.route('/volcon/v2/api/jobs/failed/report', methods=['POST'])
def failed_report():

    if not request.is_json:
        return "INVALID: Request is not json"    
    proposal = request.get_json()
    # Checks the required fields
    req_fields = ["date (Run)", "VolCon-ID", "download time", "Error"]
    req_check = l2_contains_l1(req_fields, proposal.keys())

    if req_check != []:
        return "INVALID: Lacking the following json fields to be read: "+",".join([str(a) for a in req_check])

    VolCon_ID = proposal["VolCon-ID"]
    if not mints.VolCon_ID_exists(VolCon_ID):
        return "INVALID: VolCon-ID does not exist"

    date_run = proposal["date (Run)"]
    download_time = proposal["download time"]
    received_time = mints.timnow()
    Error = proposal["Error"]
    outcome = Error

    user_token = mints.token_from_VolCon_ID(VolCon_ID)
    researcher_email = email_from_token(user_token)

    # Sends email to user, no attachments since the job did not run
    email_notification = ec.send_mail_complete(researcher_email, "BOINC job failed", ec.automatic_text(received_time, outcome, user_token, []),
                    [])

    client_IP = request.environ['REMOTE_ADDR']

    # Updates the database
    mints.failed_execution_report(VolCon_ID, date_run, download_time, Error, email_notification, client_IP)

    return "Server has processed the results"




if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5091, debug=False, threaded=True)
