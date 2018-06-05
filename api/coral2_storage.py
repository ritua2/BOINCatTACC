#!/usr/bin/env python3

"""
BASICS

CLoud storage of files on the BOINC server for using local files
"""

import os, sys
from flask import Flask, request, jsonify
import preprocessing as pp
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "/root/project/api/sandbox_files"


# Checks if Coral2 cloud storage is available
@app.route("/boincserver/v2/coral2_status")
def api_operational():
    return 'Coral2 cloud storage is available'


# Tutorial
@app.route("/boincserver/v2/coral2_tutorial")
def tutorial():

    full = { 'Port': '5060',
             'Disaclaimer': 'API usage is restricted to those with an available token',
     'Steps': {'1': 'Create a sandbox directory (skip if already own one)',
               '2': 'Upload files one by one'
              },
     'Creating a directory': 'Use the following structure: curl -d token=TOKEN  http://SERVER_IP/boincserver/v2/create_sandbox',
     'Uploading files': 'Use syntax curl  -F file=@Example_multi_submit.txt http://SERVER_IP:5060/boincserver/v2/coral2_upload/token=TOKEN'

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
    
    # Finds if the directory has already been created or not
    for sandir in os.listdir('/root/project/api/sandbox_files'):
        if TOK == sandir[4::]:
           return 'Sandbox already available'
    else:
        os.makedirs('/root/project/api/sandbox_files/DIR_'+str(TOK))
        return 'Coral2 cloud storage now available'






if __name__ == '__main__':
   app.run(host ='0.0.0.0', port = 5060)
