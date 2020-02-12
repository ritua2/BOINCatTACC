#!/usr/bin/env python3

"""
BASICS

Automated job submission for known Docker images through APIs
"""

import os, sys, shutil
import custodian as cus
from flask import Flask, request
import preprocessing as pp
from werkzeug.datastructures import ImmutableMultiDict


import custodian as cus



app = Flask(__name__)
UPLOAD_FOLDER = "/home/boincadm/project/api/sandbox_files"
ADTDP_FOLDER = "/home/boincadm/project/adtd-protocol/process_files"
FINAL_FOLDER = "/home/boincadm/project/html/user/token_data/process_files"


@app.route("/boincserver/v2/submit_known/token=<toktok>/username=<Username>", methods = ['GET', 'POST'])
def upload_file(toktok, Username):
    
    TOK = toktok
    if pp.token_test(TOK) == False:
       return 'Invalid token'
 
    if request.method != 'POST':
       return "Invalid. Submit a text file"    

    file = request.files['file']

    # Gathers all the data
    try:
        dictdata = ImmutableMultiDict(request.form).to_dict(flat='')
        app = str(dictdata["app"][0].lower())
        

        try:
            tags_used = [x.strip() for x in dictdata["topics"][0].split(";") if x.strip() != ""]

            if tags_used == []:
                tags_used = "STEM"
            else:
                tags_used = ",".join(tags_used)
                tags_used = tags_used.lower()

        except Exception as e:
            print(e)
            # Error in processing json
            tags_used = "STEM"


    except:
        return "INVALID, not all data has been provided"


    # If no app is provided, it will assume BOINC
    try:
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

    # Gets the image names
    # Although uncommon, users can write multiple commands in a single file
    with open(UPLOAD_FOLDER+'/'+new_filename, 'r') as comfil:
        for line in comfil:
            LL = line.replace('\n', '')
            if len(line.split(' ')) == 1:
                continue

            an_image = line.split(' ')[0]
            a_command = " ".join(line.split(' ')[1:])

            # Removes unnecessary content from the command
            a_command = a_command.replace("/bin/bash -c \"cd /data;", "")
            a_command = a_command.replace("python /Mov_Res.py\"", "")


            # Removes curl and wget commands
            a_command = [x.strip() for x in a_command.split(";") if ("curl -O" not in x) and ("wget" not in x)]
            a_command = ";".join(a_command)


            # Adds the topic to database
            cus.complete_tag_work(Username, TOK, tags_used, an_image, a_command, app, "terminal")

    # Adds the token at the end of the file
    with open(UPLOAD_FOLDER+'/'+new_filename, 'a') as nod:
        nod.write('\n'+str(TOK))

    if app == "boinc2docker":
        shutil.move(UPLOAD_FOLDER+'/'+new_filename, FINAL_FOLDER+'/'+new_filename)

    if app == "adtdp":
        os.remove(UPLOAD_FOLDER+'/'+new_filename)
        return "This system has been discontinued, use the new VolCon API instead"

    return "File submitted for processing\n"

    
if __name__ == '__main__':
   app.run(host = '0.0.0.0', port = 5075, debug=False, threaded=True)
