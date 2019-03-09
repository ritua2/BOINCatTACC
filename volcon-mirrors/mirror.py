"""
BASICS

APIs for a VolCon mirror
Does not receive results, they must be sent to the main BOINC server
"""



from flask import Flask, request, send_file, jsonify, after_this_request
import json
import requests
import os, shutil



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
    r = requests.post('http://'+os.environ["main_server"]+":5089/volcon/v2/api/mirrors/status/update",
            json={"key": vkey, "status":"Mirror received files", "VolCon-ID":VolCon_ID})


    return jsonify({"Status":"Succeed", "VolCon-ID":VolCon_ID})



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
            r = requests.post('http://'+os.environ["main_server"]+":5089/volcon/v2/api/mirrors/status/update",
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
        return "Job deleted successfully"
    except:
        return "INVALID, job is already being executed or does not exist, a race condition has occurred"




if __name__ == '__main__':
    app.run()
