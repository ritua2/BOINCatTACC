#!/usr/bin/env python3

"""
BASICS

Automated job submission for known Docker images through APIs
"""

import os, sys, shutil
from flask import Flask, request
import preprocessing as pp
from werkzeug.datastructures import ImmutableMultiDict


import mysql_interactions as mints




app = Flask(__name__)
UPLOAD_FOLDER = "/home/boincadm/project/api/sandbox_files"
ADTDP_FOLDER = "/home/boincadm/project/adtd-protocol/process_files"
FINAL_FOLDER = "/home/boincadm/project/html/user/token_data/process_files"



# List of TACC images and their download commands (curl/wget)
TACCIM = {"carlosred/autodock-vina:latest":"curl -O ", "carlosred/bedtools:latest":"wget",
            "carlosred/blast:latest":"curl -O ", "carlosred/bowtie:built":"curl -O ",
            "carlosred/gromacs:latest":"curl -O ", "carlosred/htseq:latest":"curl -O ",
            "carlosred/mpi-lammps:latest":"curl -O ", "carlosred/namd-cpu:latest":"curl -O ",
            "carlosred/opensees:latest":"curl -O ", "carlosred/gpu:cuda":"curl -O ", "carlosred/openfoam6:latest":"curl -O "
 }



# Finds if an image is not TACC
def image_is_TACC(image):
    if image not in TACCIM:
        return False
    return True



# Replaces characters in a string
# Returns the string with replacements
def sanitize_str_chars(s1):

    # Done manually to enforce order and simplicity
    s2 = s1.replace("\\", "\\\\")
    s2 = s2.replace("\"", "\\\"")
    s2 = s2.replace("\'", "\\\'")

    return s2



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

            if image_is_TACC(an_image):

                # Gets command
                command_itself = a_command.replace('/bin/bash -c "cd /data;', "")
                command_itself = command_itself.replace("mv ./* /root/shared/results\"", "")

                # Escapes quotes
                command_itself = sanitize_str_chars(command_itself)

                Complete_command = "/bin/bash -c \""+command_itself+" mv ./* /root/shared/results\""

            # Custom image
            else:

                # Gets command
                command_itself = a_command.replace("/bin/bash -c \"", "")
                command_itself = a_command.replace("mv ./* /root/shared/results\"", "")

                # Escapes quotes
                command_itself = sanitize_str_chars(command_itself)

                Complete_command = "/bin/bash -c \"mkdir -p /data; cd /data; "+command_itself+" mkdir -p /root/shared/results/; mv ./* /root/shared/results"


            # Adds job to database
            mints.add_boinc2docker_job(Username, TOK, tags_used, an_image, Complete_command, "boinc2docker", "cli", "Job submitted")

    # Removes file
    os.remove(UPLOAD_FOLDER+'/'+new_filename)

    return "File submitted for processing\n"

    
if __name__ == '__main__':
   app.run(host = '0.0.0.0', port = 5075, debug=False, threaded=True)
