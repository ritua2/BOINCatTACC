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
    
    # Finds if the directory has already been created or not
    for sandir in os.listdir('/root/project/api/sandbox_files'):
        if TOK == sandir[4::]:
           return 'Sandbox already available'
    else:
        os.makedirs('/root/project/api/sandbox_files/DIR_'+str(TOK))
        return 'reef cloud storage now available'


# Returns a string comma-separated, of all the files owned by a user
@app.route('/boincserver/v2/all_files/token=<toktok>')
def all_user_files(toktok):
    if pp.token_test(toktok) == False:
       return 'Invalid token'

    # Accounts for users without a sandbox yet
    try:
       AAA = []
       for afil in os.listdir('/root/project/api/sandbox_files/DIR_'+str(toktok)):

           AAA.append(afil)

       return ','.join(AAA)

    except:
       return 'Sandbox not set-up, create a sandbox first'


# Uploads one file, same syntax as for submitting batches of known commands
@app.route('/boincserver/v2/upload_reef/token=<toktok>', methods = ['GET', 'POST'])
def reef_upload(toktok):

   if pp.token_test(toktok) == False:
      return 'Invalid token'

   if request.method != 'POST':
      return 'Invalid, no file submitted'

   file = request.files['file']

   # Avoids errors with users with no sandbox assigned
   try:
      os.listdir('/root/project/api/sandbox_files/DIR_'+str(toktok))

   except:
   	  return 'User sandbox is not set-up, create a sandbox first'

    

   # Avoids empty filenames and those with commas
   if file.filename == '':
      return 'Invalid, no file uploaded'
   if ',' in file.filename:
      return "ERROR: No ',' allowed in filenames"

   # Ensures no commands within the file
   new_name = secure_filename(file.filename)
   file.save(os.path.join(UPLOAD_FOLDER+'/DIR_'+str(toktok), new_name))
   return 'File succesfully uploaded to Coral2'



if __name__ == '__main__':
   app.run(host ='0.0.0.0', port = 5060)
