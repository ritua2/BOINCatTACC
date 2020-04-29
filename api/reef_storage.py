#!/usr/bin/env python3

"""
BASICS

Cloud storage of files on the BOINC server for using local files
"""

import os, sys
from flask import Flask, request, jsonify, send_file
import preprocessing as pp
from werkzeug.utils import secure_filename
import requests



r = redis.Redis(host = '0.0.0.0', port = 6389, db =2)
app = Flask(__name__)
UPLOAD_FOLDER = "/home/boincadm/project/api/sandbox_files"


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



if __name__ == '__main__':
   app.run(host ='0.0.0.0', port = 5060, debug=False, threaded=True)
