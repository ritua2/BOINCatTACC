#!/usr/bin/env python3

"""
BASICS

Cloud storage of files on the BOINC server for using local files.
VolCon actions:
    - Process VolCon job submission from the BOINC server
    - Middle-layer operations for VolCon mirrors and clients
"""


import datetime
from flask import Flask, request, jsonify, send_file
import hashlib
import json
import os, sys
import pytz
import random
import redis
import requests
import uuid
from werkzeug.utils import secure_filename



import email_common as ec
import mirror_interactions as mirror
import mysql_interactions as mints
import preprocessing as pp




app = Flask(__name__)
r = redis.Redis(host = '0.0.0.0', port = 6389, db = 3)
UPLOAD_FOLDER = "/home/boincadm/project/api/sandbox_files"


#-------------------------------------------------------
# Reef
#-------------------------------------------------------

# Checks if reef cloud storage is available
@app.route("/boincserver/v2/reef_status")
def api_operational():
    return 'reef cloud storage is available'


# Tutorial
@app.route("/boincserver/v2/reef_tutorial")
def tutorial():

    full = { 'Port': '5060',
             'Disaclaimer': 'API usage is restricted to those with an available token',
     'Steps': {'1': 'Create a sandbox directory (skip if already own one)',
               '2': 'Upload files one by one'
              },
     'Creating a directory': 'Use the following structure: curl -d token=TOKEN  http://SERVER_IP/boincserver/v2/create_sandbox',
     'Uploading files': 'Use syntax curl  -F file=@Example_multi_submit.txt http://SERVER_IP:5060/boincserver/v2/reef_upload/token=TOKEN'

    }
    return jsonify(full)
   

# Creates a sandbox directory, returns an error if the directory does not exist
@app.route('/boincserver/v2/create_sandbox', methods = ['GET', 'POST'])
def new_sandbox():
    
    
    if request.method != 'POST':
       return 'Invalid, provide a token'

    TOK = request.form['token']
    if pp.token_test(TOK) == False:
       return 'Invalid token'
    
    resp = requests.get('http://'+os.environ['Reef_IP']+':2002/reef/create_user/'+TOK+'/'+os.environ['Reef_Key'])
    return resp.text


# Returns a string space-separated, of all the files owned by a user
@app.route('/boincserver/v2/all_files/token=<toktok>')
def all_user_files(toktok):
    if pp.token_test(toktok) == False:
       return 'Invalid token'

    resp = requests.get('http://'+os.environ['Reef_IP']+':2000/reef/all_user_files/'+os.environ['Reef_Key']+'/'+toktok)
    return resp.text


# Uploads one file, same syntax as for submitting batches of known commands
@app.route('/boincserver/v2/upload_reef/token=<toktok>', methods = ['GET', 'POST'])
def reef_upload(toktok):

   if pp.token_test(toktok) == False:
      return 'INVALID token'

   if request.method != 'POST':
      return 'INVALID, no file submitted'

   file = request.files['file']

   # Avoids empty filenames and those with commas
   if file.filename == '':
      return 'INVALID, no file uploaded'
   if ',' in file.filename:
      return "INVALID, no ',' allowed in filenames"

   resp = requests.post('http://'+os.environ['Reef_IP']+':2000/reef/upload/'+os.environ['Reef_Key']+'/'+toktok, 
          data={"filename":secure_filename(file.filename)}, files={"file": file.read()})
   return resp.content



# Allows to check the user's allocation status
# Not necessary



# Deletes a file already present in the user
@app.route('/boincserver/v2/delete_file/token=<toktok>', methods = ['GET', 'POST'])
def delete_user_file(toktok):

   if pp.token_test(toktok) == False:
      return 'Invalid token'
   if request.method != 'POST':
      return 'Invalid, provide a file to be deleted'

   try: 
      FILE = request.form['del']    
      if FILE == '':    
         return 'No file provided'
   except:
         return "Cannot parse request, 'del' entry is not present"

   resp = requests.get('http://'+os.environ['Reef_IP']+':2000/reef/delete_file/'+os.environ['Reef_Key']+'/'+toktok+'/'+FILE)
   return resp.text


# Returns a file, able to be curl/wget
@app.route('/boincserver/v2/reef/<toktok>/<FIL>')
def obtain_file(FIL, toktok):

    if pp.token_test(toktok) == False:
       return 'Invalid token'

    resp = requests.get('http://'+os.environ['Reef_IP']+':2000/reef/reef/'+os.environ['Reef_Key']+'/'+toktok+'/'+FIL)
    return resp.content


# Returns a list of all the files a user has in Reef results
@app.route("/boincserver/v2/reef_results_all/<toktok>")
def reef_results_all(toktok):
    if pp.token_test(toktok) == False:
       return 'Invalid token'

    resp = requests.get('http://'+os.environ['Reef_IP']+':2001/reef/results_all/'+os.environ['Reef_Key']+'/'+toktok)
    return resp.text


# Returns an user's results file
@app.route('/boincserver/v2/reef/results/<toktok>/<FIL>')
def results_file(FIL, toktok):
    if pp.token_test(toktok) == False:
       return 'Invalid token'

    resp = requests.get('http://'+os.environ['Reef_IP']+':2001/reef/results/'+os.environ['Reef_Key']+'/'+toktok+'/'+FIL)
    return resp.content



#-------------------
# VolCon functions
#-------------------

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



# Finds present day in CST
def present_day():
    UTC_date = datetime.datetime.utcnow()

    tz1 = pytz.timezone("UTC")
    tz2 = pytz.timezone("America/Chicago")

    UTC_date = tz1.localize(UTC_date)
    CST_date = UTC_date.astimezone(tz2)

    return CST_date.strftime("%Y-%m-%d")


# Currently, tokens are also emails
def email_from_token(token):
    return token



#-------------------------------------------------------
# Job processing and communication with VolCon clients
#-------------------------------------------------------

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

    # Saves the location of the file
    mints.update_results_path_apache(VID, location+"/"+new_name)

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
        attachments = mints.read_results_path_apache(VolCon_ID)
        result_error = "No errors retrieving data"

    if Error == "":
        Error = None
        outcome = "Success"
        specific_command_errors = None
        # Uploads the data to Reef
        requests.post('http://'+os.environ['Reef_IP']+':2001/reef/result_upload/'+os.environ['Reef_Key']+'/'+user_token,
                    files={"file": open(attachments[0], "rb")})
        mints.update_results_path_reef(VolCon_ID, attachments[0])
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



#-----------------------------------------------------------
# Middle-layer interactions with VolCon mirrors and clients
#-----------------------------------------------------------


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
   app.run(host ='0.0.0.0', port = 5060, debug=False, threaded=True)
