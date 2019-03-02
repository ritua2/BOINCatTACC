#!/usr/bin/env python3

"""
BASICS

Processes all commands submitted through the web interface and creates a file ready for BOINC processing
"""

import os, sys, shutil
import json
from flask import Flask, request, jsonify, send_file
import preprocessing as pp
import custodian as cus




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
            "carlosred/opensees:latest":"curl -O ", "carlosred/gpu:cuda":"curl -O ", "carlosred/openfoam6:latest":"curl -O "
 }


# Finds if an image is not TACC
def image_is_TACC(image):
    if image not in TACCIM.keys():
        return False
    return True


# List of extra commands needed for some files
EXIM = {"carlosred/gromacs:latest":"source /usr/local/gromacs/bin/GMXRC.bash; ", "carlosred/openfoam6:latest":". /opt/openfoam6/etc/bashrc; "}


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
        boapp = dictdata['Boapp'].lower()
        Reefil = dictdata["Files"]
        Image = dictdata["Image"]
        Custom = dictdata["Custom"]
        Command = dictdata["Command"]

    except:
        return "INVALID, json lacks at least one field (keys: Token, Boapp, Files, Image, Custom, Command)"

    if pp.token_test(TOK) == False:
        return "INVALID token"

    # Checks if user wants boinc2docker or adtd-p
    try:
        if (boapp != "boinc2docker") and (boapp != "adtdp"):
            return "INVALID application"

    except:
        return "INVALID, application not provided"

    if (Custom != "Yes") and (Custom != "No"):
        return "INVALID, Custom value can only be [Yes/No]"

    if ("Custom" == "No") and (not image_is_TACC(Image)):
        return "INVALID, Image \'"+Image+"\' is not provided by TACC"

    # Writes the commands to a random file
    new_filename = pp.random_file_name()


    with open(UPLOAD_FOLDER+new_filename, "w") as comfil:
        comfil.write(Image + " /bin/bash -c ")

        # Custom images require more work because it must be ensured the results will be back
        if Custom == "Yes":
            # Creates a new working directory
            comfil.write("\"mkdir -p /data; cd /data; ")
            # Adds the files
            for FF in Reefil:
                comfil.write(get_reef_file(Image, TOK, FF)+" ")

            comfil.write(Command+" mkdir -p /root/shared/results/; mv ./* /root/shared/results\"")
            comfil.write("\n"+str(TOK))

        elif Custom == "No":
            comfil.write("\"")
            comfil.write(extra_image_commands(Image))
            # Adds the files
            for FF in Reefil:
                comfil.write(get_reef_file(Image, TOK, FF)+" ")

            comfil.write(Command+" python /Mov_Res.py\"")
            comfil.write("\n"+str(TOK))

    # Submits the file for processing
    if boapp == "boinc2docker":
        shutil.move(UPLOAD_FOLDER+new_filename, BOINC_FOLDER+new_filename)
    if boapp == "adtdp":
        shutil.move(UPLOAD_FOLDER+new_filename, ADTDP_FOLDER+new_filename)

    return "Commands submitted for processing"


if __name__ == '__main__':
    # Outside of container
    app.run(host = '0.0.0.0', port = 6035, debug=False, threaded=True)
