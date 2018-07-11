#!/usr/bin/env python3

"""
BASICS

Processes all commands submitted through the web interface and creates a file ready for BOINC processing
"""

import os, sys, shutil
import json
from flask import Flask, request, jsonify, send_file
import preprocessing as pp
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
import redis



app = Flask(__name__)
ADTDP_FOLDER = "/root/project/adtd-protocol/process_files/"
BOINC_FOLDER = "/root/project/html/user/token_data/process_files/"
UPLOAD_FOLDER = "/root/project/api/"
SERVER_IP = os.environ['SERVER_IP']


@app.route("/boincserver/v2/api/process_web_jobs", methods=['GET', 'POST'])
def process_web_jobs():

    if request.method != 'POST':
       return "INVALID, no data provided"  


    # Only for internal use, all other use will return an error
    if (request.remote_addr != '0.0.0.0') and (request.remote_addr != SERVER_IP):
        return "INVALID, API for internal use only"

    dictdata = ImmutableMultiDict(request.form).to_dict(flat='')

    TOK = dictdata["token"][0]
    if pp.token_test(TOK) == False:
        return "INVALID token"

    # Checks if user wants boinc2docker or adtd-p
    try:
        boapp = dictdata['boapp'][0].lower()
        if (boapp != "boinc2docker") and (boapp != "adtdp"):
            return "INVALID application"

    except:
        return "INVALID, application not provided"

    file = request.files['file']
    # Files must be JSON
    if file.filename == '':
        return "INVALID, no file provided"
    if file.filename.split('.')[-1] != 'json':
       return "File type invalid, only JSON files are acccepted"

    # Writes the commands to a random file
    new_filename = pp.random_file_name()
    file.save(UPLOAD_FOLDER+new_filename)


    try:
        ff = open(UPLOAD_FOLDER+new_filename)
        command_data = json.load(ff.read())
        ff.close()
    except:
        os.remove(UPLOAD_FOLDER+new_filename)
        return "INVALID, json could not be parsed"

    # All JSON files must have the following:
    # Image, Image is custom, Command
    try:
        Image = command_data["Image"]
        Custom = command_data["Custom"]
        Command = command_data["Command"]
    except:
        os.remove(UPLOAD_FOLDER+new_filename)
        return "INVALID, json lacks at least one field (keys: Image, Custom, Command)"


    with open(UPLOAD_FOLDER+new_filename, "w") as comfil:
        comfil.write(Image + "/bin/bash -c ")
        Invalid_Custom = False

        # Custom images require more work because we must ensure the results will be back
        if Custom == "Yes":
            comfil.write("\""+Command+"; mkdir -p /root/shared/results/; mv ./* /root/shared/results\"")
            comfil.write("\n"+str(TOK))

        elif Custom == "No":
            comfil.write("\"cd /data; "+Command+"; python /Mov_Res.py\"")
            comfil.write("\n"+str(TOK))

        else:
            Invalid_Custom = True

    if Invalid_Custom:
        # There is no need to keep the file after if has been deleted
        os.remove(UPLOAD_FOLDER+new_filename)
        return "INVALID, custom value can only be Yes/No"

    # Submits the file for processing
    if boapp == "boinc2docker":
        shutil.move(UPLOAD_FOLDER+new_filename, BOINC_FOLDER+new_filename)
    if boapp == "adtdp":
        shutil.move(UPLOAD_FOLDER+new_filename, ADTDP_FOLDER+new_filename)

    return "Commands submitted for processing"


if __name__ == '__main__':
   app.run(host = '0.0.0.0', port = 5096)
