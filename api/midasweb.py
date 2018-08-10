#!/usr/bin/env python3

"""
BASICS

Processes MIDAS jobs submitted through the web interface
"""

from flask import Flask, request, jsonify
import shutil, os, sys
import tarfile, zipfile
import re
import preprocessing as pp
from midas_processing import midas_reader as mdr
from werkzeug.utils import secure_filename
import redis


r = redis.Redis(host = '0.0.0.0', port = 6389, db=2)
app = Flask(__name__)
UPLOAD_FOLDER = "/root/project/api/sandbox_files"
boapp = "boinc2docker" # boinc2docker by default



# Writes information using MIDAS syntax
# [UNO]: DOS
def midsyn(UNO, DOS):
    return "["+str(UNO)+"] "+str(DOS)+"\n"


# Processes a user entered command into a bash file to be executed as is
# If there are C++ libraries, then all C++ codes will include the libraries as a side-effect
# COMS (arr)(str)
# tmpdir (str): temporary directory
def comproc(COM, tempdir):

    filnam = "exec.sh"
    if filnam in os.listdir(tempdir):
        raise SyntaxError("exec.sh is a reserved filename")

    with open(tempdir+filnam) as comfil:
        for com in COMS:
            if (boapp == "adtdp") and "g++" in com:
                comfil.write("g++ -I ./cget/include/ "+ com.replace("g++", '') + "\n")
                continue
            comfil.write(com+'\n')


# Writes a valid README using the contents in the JSON object
# Returns a string with the contents
def verne(jdat, tempdir):
    rcon = ""
    rcon += midsyn("OS", jdat["operating_system"])
    progs = jdat["programming_language"]
    for lang in progs:
        rcon += midsyn("LANGUAGE", lang.replace("Plus", "+"))
    if boapp == "adtdp":
        rcon += midsyn("LANGUAGE", "C++ cget")

    # Libraries
    for lib in jdat["library_list"]["python"]:
        rcon += midsyn("LIBRARY", "python: "+lib)
    for lib in jdat["library_list"]["cPlusPlus"]:
        rcon += midsyn("LIBRARY", "C++ cget: "+lib)

    # User setup
    if jdat["setup_filename"] != "":
        rcon += midsyn("USER_SETUP", jdat["setup_filename"])

    # Commands, separated by ;
    # Enforces that C, c++, fortran are captured by their gnu compilers
    commands = dictdata["command_lines"]
    if ("fortran" in progs) and ("gfortran" not in commands):
        raise SyntaxError("Fortran must be compiled using gfortran")
    if ("c" in progs) and ("gcc" not in commands):
        raise SyntaxError("C must be compiled using gcc")
    if ("cPlusPlus" in progs) and ("g++" not in commands):
        raise SyntaxError("Fortran must be compiled using g++")

    commands = commands.split(';')
    comproc(commands, tempdir)
    rcon += misdyn("COMMAND", "bash: exec.sh")

    # Output files
    for ofil in jdat["output_file"]:
        rcon += misdyn("OUTPUT", ofil)

    return rcon




# Processes MIDAS jobs through the web interface

@app.route("/boincserver/v2/api/process_midas_jobs", methods=['POST'])
def process_midas_jobs():

    try:
        dictdata = request.get_json()
    except:
        return "INVALID, JSON could not be parsed"

    try:
        TOK = dictdata["token"]
        tmp_dir = dictdata["folder_name"]
        OS = dictdata["operating_system"]
        prolangs = dictdata["programming_language"]
        libs = dictdata["library_list"]
        setfiles = jdat["setup_filename"]
        outfiles = dictdata["output_file"]
        coms = dictdata["command_lines"]

    except:
        return "INVALID, json lacks at least one field (keys: Token, Boapp, Files, Image, Custom, Command)"

    if  pp.token_test(TOK) == False:
        shutil.rmtree(TMP)
        return 'INVALID, invalid token'

    # MIDAS files are stored in a temporary folder
    TMP = "/tmp/"+tmp_dir+'/'

    if 'README.txt' in os.listdir(TMP):
        return "INVALID, README.txt is a MIDAS reserved file. Please, remove it and try again"

    for file in os.listdir(TMP):

        if (file.split(".")[-1] == "tgz") or (".".join(file.split(".")[::-1][:2:][::-1]) == "tar.gz"):
            # Takes the contents out and deletes the tar
            try:
                tar = tarfile.open(file)
                tar.extractall(TMP)
                tar.close()
                os.remove(TMP+file)
                continue
            except:
                shutil.rmtree(TMP)
                return "INVALID, cannot open tar file"

        if (file.split(".")[-1] == "zip"):
            try:
                zip_ref = zipfile.ZipFile(TMP+file, 'r')
                zip_ref.extractall(TMP)
                zip_ref.close()
                os.remove(TMP+file)
            except:
                shutil.rmtree(TMP)
                return "INVALID, cannot open zip file"

    # The application is adtdp if using c++ libraries
    if libs['cPlusPlus'] != []:
        boapp = "adtdp"

    # Creates an acceptable README
    with open(TMP+"README.txt") as readme:
        try:
            readme.write(verne(dictdata, TMP))
        except Exception as e:
            shutil.rmtree(TMP)
            return "INVALID, "+e

    # Validates if the file can be processed
    if not mdr.valid_README(TMP+'/README.txt'):
        shutil.rmtree(TMP)
        return 'INVALID, README in user input'

    if not mdr.valid_OS(TMP+'/README.txt'):
        shutil.rmtree(TMP)
        return 'INVALID, OS is not accepted'
        
    if not mdr.present_input_files(TMP):
        shutil.rmtree(TMP)
        return 'INVALID, Not all input files for commands are present'

    if not mdr.valid_language(TMP+'/README.txt'):
        shutil.rmtree(TMP)
        return 'INVALID, Language is not accepted'

    # Avoids cases where no libraries are needed at all
    if (not mdr.install_libraries(TMP+'/README.txt')) and (mdr.install_libraries(TAR_PATH+'/README.txt') != []):
        shutil.rmtree(TMP)
        return 'INVALID, Language does not support libraries'

    # Moves the directory to MIDAS and processes it
    ALL_USER_DATA = os.listdir('/root/project/api/sandbox_files/DIR_'+str(toktok))
    while True:
        new_MID = 'MID_'+pp.random_dir_name()
        if new_MID not in ALL_USER_DATA:
            break

    MIDAS_PATH = UPLOAD_FOLDER+'/DIR_'+str(TOK)+'/'+new_MID
    shutil.copytree(TMP, MIDAS_PATH)

    # Creates a redis database with syntax {TOKEN}.{MID_DIRECTORY}
    r.set(TOK+';'+new_MID, boapp)

    return 'File submitted for processing'



if __name__ == '__main__':
    # Outside of container
    app.run(host = '0.0.0.0', port = 6075)
