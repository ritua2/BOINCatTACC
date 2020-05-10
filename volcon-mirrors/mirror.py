"""
BASICS

APIs for a VolCon mirror
Does not receive results, they must be sent to the main BOINC server
"""



from flask import Flask, request, send_file, jsonify, after_this_request
import json
import requests
import os, shutil
import urllib.parse
from werkzeug.utils import secure_filename




app = Flask(__name__)


skey = os.environ["SERVER_ID"]
vkey = os.environ["volcon_key"]
PATH="/mirror"


# Given two lists, returns those values that are lacking in the second
# Empty if list 2 contains those elements
def l2_contains_l1(l1, l2):

    return[elem for elem in l1 if elem not in l2]


# Checks if the password is correct
def bad_password(password):

    if password == skey:
        return False
    return True



# Can be called to ensure that a mirror is available
@app.route("/volcon/mirror/v2/api/available", methods=['GET'])
def available():
    return "Ok"



# Receives a job from the server, stores the files
# TACC images are not stored, volcon clients should pull them if not available
# Runs public dockerhub images, not valid for MIDAS jobs
@app.route("/volcon/mirror/v2/api/public/receive_job_files", methods=['POST'])
def receive_job_files():

    if not request.is_json:
        return "INVALID: Request is not json"

    proposal = request.get_json()

    # Checks the required fields
    req_fields = ["key", "Image", "Command", "GPU", "VolCon_ID", "TACC"]
    req_check = l2_contains_l1(req_fields, proposal.keys())

    if req_check != []:
        return "INVALID: Lacking the following json fields to be read: "+",".join([str(a) for a in req_check])

    if bad_password(proposal["key"]):
        return "INVALID: incorrect password"

    VolCon_ID = proposal["VolCon_ID"]

    # Removes sensitive information
    proposal.pop("key", None)

    # Makes a new directory with the files
    os.mkdir(PATH+"/"+VolCon_ID)


    # Saves the commands there
    with open(PATH+"/"+VolCon_ID+"/meta.json", "w") as ff:
        json.dump(proposal, ff)

    # Updates the main server that the job is currently being run
    r = requests.post('http://'+os.environ["main_server"]+":5060/volcon/v2/api/mirrors/status/update",
            json={"key": vkey, "status":"Mirror received files", "VolCon-ID":VolCon_ID})


    return jsonify({"Status":"Succeed", "VolCon-ID":VolCon_ID})



# Receives files for a MIDAS job
# Does not support a hierarchical structure, VolCon is not designed for continuous file storage
@app.route("/volcon/mirror/v2/api/MIDAS/receive_files/<VolCon_ID>/key=<mirrorkey>", methods=['POST'])
def receive_MIDAS_files(VolCon_ID, mirrorkey):

    # Guaranteed to have a sequential call, no need to check for race conditions and possible error creating the directory
    if bad_password(mirrorkey):
        return "INVALID: incorrect password"

    if "file" not in request.files.keys():
        return "INVALID, file not provided"

    try:
        file = request.files["file"]
    except:
        return "INVALID, file is too large, exceeded 300 s timeout for file processing"

    storage_location = PATH+"/"+VolCon_ID+"-files"
    if not os.path.exists(storage_location):
        os.mkdir(storage_location)

    # Saves the file using secure filename
    new_name = secure_filename(file.filename)
    # Saves the file
    file.save(storage_location+"/"+new_name)
    return jsonify({"Status":"Succeed", "VolCon-ID":VolCon_ID})



# Returns a file for a MIDAS job and deletes it after returning it to the user
# Also deletes the directory if it does not contain any more files
@app.route("/volcon/mirror/v2/api/public/request_job_file/<volcon_id>/<filename>", methods=['GET'])
def request_job_file(volcon_id, filename):

    # File may contain characters that are not possible without URL encoding
    filename = urllib.parse.unquote(filename)
    if not os.path.isfile(PATH+"/"+volcon_id+"-files/"+filename):
        return "INVALID credentials"

    @after_this_request
    def remove_files(response):

        # Deletes the file
        os.remove(PATH+"/"+volcon_id+"-files/"+filename)
        if os.listdir(PATH+"/"+volcon_id+"-files/") == 0:
            os.rmdir(PATH+"/"+volcon_id+"-files/")
        return response

    return send_file(PATH+"/"+volcon_id+"-files/"+filename)

# curl http://149.165.170.140:7000/volcon/mirror/v2/api/public/request_job_file/echo1/thing.txt

# Request of job information for a TACC image job
# Returns a json object with the information
# Then deletes the directory to save space
@app.route("/volcon/mirror/v2/api/public/request_job/<volcon_id>", methods=['GET'])
def request_job(volcon_id):

    if not os.path.exists(PATH+"/"+volcon_id):
        return "INVALID credentials"

    @after_this_request
    def remove_files(response):
        try:
            shutil.rmtree(PATH+"/"+volcon_id)

            # Notify the server that the job is being run
            r = requests.post('http://'+os.environ["main_server"]+":5060/volcon/v2/api/mirrors/status/update",
                json={"key": vkey, "status":"Job files requested", "VolCon-ID":volcon_id})

        except:
            pass
        return response

    return send_file(PATH+"/"+volcon_id+"/meta.json")



# Deletes a job
@app.route("/volcon/mirror/v2/api/public/delete_job/<volcon_id>/<sid>", methods=['GET'])
def delete_job(volcon_id, sid):

    if sid != skey:
        return "INVALID credentials"

    if not os.path.exists(PATH+"/"+volcon_id):
        return "INVALID, job is already being executed or does not exist"

    try:
        shutil.rmtree(PATH+"/"+volcon_id)

        # Also deletes any files associated with it
        if os.path.isdir(PATH+"/"+volcon_id+"-files"):
            shutil.rmtree(PATH+"/"+volcon_id+"-files")

        return "Job deleted successfully"
    except:
        return "INVALID, job is already being executed or does not exist, a race condition has occurred"




if __name__ == '__main__':
    app.run()
