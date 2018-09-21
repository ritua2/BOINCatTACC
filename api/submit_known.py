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

    # Gathers all the data
    try:
        dictdata = ImmutableMultiDict(request.form).to_dict(flat='')
        app = str(dictdata["app"][0].lower())
        # Gets the list of topics/subtopics
        Tops = [j for j in dictdata.keys() if j != "app"]
        # Each topic will be defined by Topic: subtopics
        # Subtopics are separated by commas
        TST = {} # Topics structure

        for one_top in Tops:
            TST[one_top] = [zz for zz in dictdata[one_top][0].upper().split(',') if zz != '']

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
    Im_Names = []
    with open(UPLOAD_FOLDER+'/'+new_filename, 'r') as comfil:
        for line in comfil:
            LL = line.replace('\n', '')
            if len(line.split(' ')) == 1:
                continue
            Im_Names.append(line.split(' ')[0])

    # Adds the token at the end of the file
    with open(UPLOAD_FOLDER+'/'+new_filename, 'a') as nod:
        nod.write('\n'+str(TOK))

    AA = ''
    if app == "boinc2docker":
        # Adds the topic to database
        for an_image in Im_Names:
            AA += cus.complete_tag_work(an_image, TST, jobsub=len(Im_Names))
        shutil.move(UPLOAD_FOLDER+'/'+new_filename, FINAL_FOLDER+'/'+new_filename)
    if app == "adtdp":
        shutil.move(UPLOAD_FOLDER+'/'+new_filename, ADTDP_FOLDER+'/'+new_filename)

    return "File submitted for processing\n"+AA

    
if __name__ == '__main__':
   app.run(host = '0.0.0.0', port = 5075)
