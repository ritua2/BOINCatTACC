"""
BASICS

Processes job submissions from the BOINC server
"""


import datetime
from flask import Flask, request
import hashlib
import json


app = Flask(__name__)


# Checks a password withe respective type of Volcon system (mirrors)
def bad_password(volcon_type, given_password):

    try:
        system_key = r.hget(volcon_type, "Organization Token").decode("UTF-8")
        hp = password = hashlib.sha256(given_password.encode('UTF-8')).hexdigest()

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
@app.route('/volcon/v2/api/jobs/tacc', methods=['POST'])
def tacc_jobs():

    





if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5091, debug=False, threaded=True)


