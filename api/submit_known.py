#!/usr/bin/env python3

"""
BASICS

Automated job submission for known Docker images through APIs
"""

import os, sys, shutil
from flask import Flask, request
import preprocessing as pp



app = Flask(__name__)
UPLOAD_FOLDER = "/root/project/api/sandbox_files"
ADTDP_FOLDER = "/root/project/adtd-protocol/process_files"
FINAL_FOLDER = "/root/project/html/user/token_data/process_files"


@app.route("/boincserver/v2/submit_known/token=<toktok>", methods = ['GET', 'POST'])
def upload_file(toktok):
    
    TOK = toktok
    if pp.token_test(TOK) == False:
       return 'Invalid token'
 
    if request.method != 'POST':
       return "Invalid. Submit a text file"    

    file = request.files['file']

    # If no app is provided, it will assume BOINC
    try:
        app = request.form["app"].lower()
        if (app != "boinc2docker") and (app != "adtdp"):
            return "INVALID app"
    except:
        app = "boinc2docker"

    # Avoids empty files and non-text files
    if file.filename == '':
       return 'No file submitted'
    if file.filename.split('.')[-1] != 'txt':
       return "File type invalid, only text files are acccepted"

    # Randomizes the file name to avoid matches
    new_filename = pp.random_file_name()
    file.save(os.path.join(UPLOAD_FOLDER, new_filename))
    # Adds the token at the end of the file
    with open(UPLOAD_FOLDER+'/'+new_filename, 'a') as nod:
        nod.write('\n'+str(TOK))

    if app == "boinc2docker":
        shutil.move(UPLOAD_FOLDER+'/'+new_filename, FINAL_FOLDER+'/'+new_filename)
    if app == "adtdp":
        shutil.move(UPLOAD_FOLDER+'/'+new_filename, ADTDP_FOLDER+'/'+new_filename)

    return "File submitted for processing"

    
if __name__ == '__main__':
   app.run(host = '0.0.0.0', port = 5075)
