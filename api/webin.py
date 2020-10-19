#!/usr/bin/env python3

"""
BASICS

Processes all commands submitted through the web interface and creates a file ready for BOINC processing
"""

import os, sys, shutil
import json
from flask import Flask, request, jsonify, send_file, abort
import mirror_interactions as mirror
import mysql_interactions as mints
import preprocessing as pp
import custodian as cus
import uuid




app = Flask(__name__)
ADTDP_FOLDER = "/home/boincadm/project/adtd-protocol/process_files/"
BOINC_FOLDER = "/home/boincadm/project/html/user/token_data/process_files/"
UPLOAD_FOLDER = "/home/boincadm/project/api/"
SERVER_IP = os.environ['SERVER_IP']


# List of TACC images and their download commands (curl/wget)
TACCIM = {"carlosred/autodock-vina:latest":"curl -O ", "carlosred/bedtools:latest":"wget",
            "carlosred/blast:latest":"curl -O ", "carlosred/bowtie:built":"curl -O ",
            "carlosred/gromacs:latest":"curl -O ", "carlosred/htseq:latest":"curl -O ",
            "carlosred/mpi-lammps:latest":"curl -O ", "carlosred/namd-cpu:latest":"curl -O ",
            "saumyashah/opensees:latest":"curl -O ", "carlosred/gpu:cuda":"curl -O ", "carlosred/openfoam6:latest":"curl -O "
 }


# Finds if an image is not TACC
def image_is_TACC(image):
    if image not in TACCIM.keys():
        return False
    return True


# List of extra commands needed for some files
EXIM = {"carlosred/gromacs:latest":"source /usr/local/gromacs/bin/GMXRC.bash && ",
        "carlosred/openfoam6:latest":"source /opt/OpenFOAM/OpenFOAM-6/etc/bashrc && "}


# Returns a files download type
# If custom, it uses curl -O
# IMIM (str): Image name

def howto_download(IMIM):

    if IMIM not in TACCIM.keys():
        # File is custom
        return "curl -O "

    return TACCIM[IMIM]


# Adds extra commands depending on the image
def extra_image_commands(IMIM):

    if IMIM not in EXIM:
        return ''

    return EXIM[IMIM]



# Gives precise instructions on how to download a file from Reef
# If it is a compressed file, it also uncompresses it
# TOK (str): Token, guaranteed to work, since checked before
# filnam (str): File name

def get_reef_file(IMIM, TOK, filnam):

    # Calls the file from Reef
    Com = howto_download(IMIM)+" http://"+os.environ["SERVER_IP"]+":5060/boincserver/v2/reef/"+TOK+"/"+filnam+";"

    # If the file is zipped or tar, it must be uncompressed
    if (filnam.split(".")[-1] == "tgz") or (".".join(filnam.split(".")[::-1][:2:][::-1]) == "tar.gz"):
        Com += "tar -xzf "+filnam+";"
    if (filnam.split(".")[-1] == "zip"):
        Com += "unzip "+filnam+";"

    return Com




# Replaces characters in a string
# Returns the string with replacements
def sanitize_str_chars(s1):

    # Done manually to enforce order and simplicity
    s2 = s1.replace("\\", "\\\\")
    s2 = s2.replace("\"", "\\\"")
    s2 = s2.replace("\'", "\\\'")

    return s2


@app.route("/boincserver/v2/api/process_web_jobs", methods=['GET', 'POST'])
def process_web_jobs():

    if request.method != 'POST':
       return "INVALID, no data provided"  


    try:
        dictdata = request.get_json()
    except:
        return "INVALID, JSON could not be parsed"


    try:
        TOK = dictdata["Token"]
        Reefil = dictdata["Files"]
        Image = dictdata["Image"]
        Custom = dictdata["Custom"]
        Command = dictdata["Command"]
        Username = dictdata["Username"]

        if "priority" not in dictdata.keys():
            PRIORITY = "Middle"
        else:
            PRIORITY = dictdata["priority"]
    except:
        return "INVALID, json lacks at least one field (keys: Token, Boapp, Files, Image, Custom, Command, Username)"

    if pp.token_test(TOK) == False:
        return "INVALID token"

    # Checks the list of Commands to ensure their correct execution
    Command = ';'.join([C for C in Command.split(';') if (C != '') and (C.count(C[0]) != len(C)) ]) +';'

    boapp = "boinc2docker"
    if Image == "carlosred/gpu:cuda":
        boapp = "volcon"

    if (Custom != "Yes" ) and (Custom != "No"):
        return abort(422) # Incorrect API

    if not image_is_TACC(Image):
        Custom = "Yes"
        # Gets the tags
        try:
            tags_used = [x.strip() for x in dictdata["topics"].split(";") if x.strip() != ""]

            if tags_used == []:
                tags_used = "STEM"
            else:
                tags_used = ",".join(tags_used)
                tags_used = tags_used.lower()

        except Exception as e:
            print(e)
            # Error in processing json
            tags_used = "STEM"

    else:
        # Default tag: STEM
        tags_used = "STEM"


    if boapp == "boinc2docker":
        # Writes the commands to a random file
        new_filename = pp.random_file_name()

        Complete_command = ""

        # Custom images require more work because it must be ensured the results will be back
        if Custom == "Yes":
            # Creates a new working directory
            Complete_command += "mkdir -p /data; cd /data; "
            # Adds the files
            for FF in Reefil:

                # Skips unnecessary files
                if FF == "":
                    break
                Complete_command += get_reef_file(Image, TOK, FF)+" "

            Complete_command += Command+" mkdir -p /root/shared/results/; mv ./* /root/shared/results"

        elif Custom == "No":
            # Adds the files
            for FF in Reefil:

                # Skips unnecessary files
                if FF == "":
                    break
                Complete_command += get_reef_file(Image, TOK, FF)+" "

            Complete_command += Command +" mv ./* /root/shared/results"


        # Replaces certain characters
        Complete_command = " /bin/bash -c \""+sanitize_str_chars(Complete_command)+"\""
        mints.add_boinc2docker_job(Username, TOK, tags_used, Image, Complete_command, boapp, "web", "Job submitted")

        # Old way
        # shutil.move(UPLOAD_FOLDER+new_filename, BOINC_FOLDER+new_filename)


    if boapp == "volcon":
        
        # Only CUDA requires a GPU
        # Custom images are also assumed to not require a GPU TODO TODO TODO TODO
        if Image == "carlosred/gpu:cuda":
            GPU = 1
        else:
            GPU = 0

        VolCon_ID = uuid.uuid4().hex

        COMMANDS = ""

        if Custom == "Yes":
            TACC = 0
            COMMANDS += "mkdir -p /data; cd /data; "
            for FF in Reefil:
                if FF == '':
                    break
                COMMANDS += get_reef_file(Image, TOK, FF)+" "

            # Splits the commands and ensures that they are run in /data
            newcoms = ";".join(["cd /data && "+x for x in Command.split(";")])

            COMMANDS += newcoms+" mkdir -p /root/shared/results/; mv /data/* /root/shared/results"

        else:
            TACC = 1
            for FF in Reefil:
                if FF == '':
                    break
                COMMANDS += get_reef_file(Image, TOK, FF)+" "
            COMMANDS += ";".join([extra_image_commands(Image) +z for z in Command.split(";")])+" mv ./* /root/shared/results"

        COMMANDS = " /bin/bash -c \""+COMMANDS+"\""

        job_info = {"Image":Image, "Command":COMMANDS, "TACC":TACC, "GPU":GPU, "VolCon_ID":VolCon_ID, "public":1}

        # Updates the job in the database
        mints.add_job(TOK, Image, COMMANDS, GPU, VolCon_ID, PRIORITY, 1, tags_used, Username, "web")
        # Pushes job information to mirrors
        mirror.upload_job_to_mirror(job_info)


    return "Commands submitted for processing"



if __name__ == '__main__':
    # Outside of container
    app.run(host = '0.0.0.0', port = 6035, debug=False, threaded=True)
