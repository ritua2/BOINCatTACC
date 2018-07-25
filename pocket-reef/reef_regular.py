#!/usr/bin/env python3

"""
BASICS

Returns user files or information about them
"""

import os, sys
from flask import Flask, request, jsonify, send_file
import base_functions as bf
from werkzeug.utils import secure_filename


app = Flask(__name__)
REEF_FOLDER = os.environ['Reef_Path']+"/sandbox/"


# Checks if reef cloud storage is available
@app.route('/reef/status')
def api_operational():
    return 'External Reef cloud storage is available'


# Returns a string comma-separated, of all the files owned by a user
@app.route('/reef/all_user_files/<rkey>/<toktok>')
def all_user_files(toktok, rkey):

    if not bf.valid_key(rkey):
        return "INVALID key"
    if str('DIR_'+toktok) not in os.listdir(REEF_FOLDER):
       return 'INVALID, User directory does not exist'


    # Accounts for users without a sandbox yet
    try:
       AAA = []
       for afil in os.listdir(REEF_FOLDER+'DIR_'+str(toktok)):

           AAA.append(afil)

       return ' '.join(AAA)

    except:
       return 'Sandbox not set-up, create a sandbox first'


# Uploads one file
@app.route("/reef/upload/<rkey>/<toktok>", methods=['POST'])
def result_upload(toktok, rkey):

    if not bf.valid_key(rkey):
        return "INVALID key"
    if str('DIR_'+toktok) not in os.listdir(REEF_FOLDER):
       return 'INVALID, User directory does not exist'

    if request.method != 'POST':
       return 'INVALID, no file submitted'

    file = request.files['file']
    fnam = request.form['filename']

    # Avoids empty filenames and those with commas
    if file.filename == '':
       return 'INVALID, no file uploaded'
    if ',' in file.filename:
       return "INVALID, no ',' allowed in filenames"

    # Ensures no commands within the filename
    new_name = secure_filename(fnam)
    file.save(os.path.join(REEF_FOLDER+'DIR_'+str(toktok), new_name))
    return 'File succesfully uploaded to Reef'


# Deletes a file already present in the user
@app.route('/reef/delete_file/<rkey>/<toktok>/<FILE>')
def delete_user_file(toktok, rkey, FILE):

    if not bf.valid_key(rkey):
        return "INVALID key"
    if str('DIR_'+toktok) not in os.listdir(REEF_FOLDER):
       return 'INVALID, User directory does not exist'

    try:       
       os.remove(REEF_FOLDER+'DIR_'+str(toktok)+'/'+str(FILE))
       return 'File succesfully deleted from reef storage'

    except:
       return 'File is not present in Reef'


# Returns a file
@app.route('/reef/reef/<rkey>/<toktok>/<FIL>')
def results_file(rkey, toktok, FIL):

    if not bf.valid_key(rkey):
        return "INVALID key"
    if str('DIR_'+toktok) not in os.listdir(REEF_FOLDER):
       return 'INVALID, User directory does not exist'

    USER_DIR = REEF_FOLDER+'DIR_'+str(toktok)+'/'
    if str(FIL) not in os.listdir(USER_DIR):
       return 'INVALID, File not available'

    return send_file(USER_DIR+str(FIL))



if __name__ == '__main__':
   app.run(host ='0.0.0.0', port = 2000)
