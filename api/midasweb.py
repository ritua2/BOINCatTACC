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


import mysql_interactions as mints



app = Flask(__name__)
UPLOAD_FOLDER = "/home/boincadm/project/api/sandbox_files"
valid_compilers = ['gcc', 'g++', 'gfortran']


# Finds if a string exists in a list of strings
def sinlis(goal_str, lstr):

    for member in lstr:
        if goal_str in member:
            return True

    return False


# Writes information using MIDAS syntax
# [UNO]: DOS
def midsyn(UNO, DOS):
    return "["+str(UNO)+"] "+str(DOS)+"\n"


# Creates an extra user-setup files if gcc, gfortran or g++ are included
# Returns the list of commands at the end
# COMS (arr)(str)
# tempdir (str): temporary directory
def extra_uset(COMS, tempdir, boapp):

    filnam = "compile_instructions.sh"
    # List of commands after removing compilers
    C2 = []

    if filnam in os.listdir(tempdir):
        raise SyntaxError("compile_instructions.sh is a reserved filename")

    with open(tempdir+filnam, 'w') as exfil:

        nocom = True

        for com in COMS:
            if any(valcom in com for valcom in valid_compilers):
                nocom = False
                # C++ is different since it may require cget libraries
                if (boapp == "adtdp") and ("g++" in com):
                    exfil.write("g++ -I ./cget/include/ "+ com.replace("g++", '') + "\n")
                    continue

                exfil.write(com+'\n')
                continue
            C2.append(com)

    # If there were no compile instructions
    if nocom:
        os.remove(tempdir+filnam)

    return C2


# Processes a user entered command into a bash file to be executed as is
# If there are C++ libraries, then all C++ codes will include the libraries as a side-effect
def comproc(COMS, tempdir, boapp):

    filnam = "exec.sh"

    if filnam in os.listdir(tempdir):
        raise SyntaxError("exec.sh is a reserved filename")

    with open(tempdir+filnam, 'w') as comfil:
        for com in COMS:
            comfil.write(com+'\n')


# Writes a valid README using the contents in the JSON object
# Returns a string with the contents
def verne(jdat, tempdir, boapp):
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
    commands = jdat["command_lines"].replace("&&", ';').split(';')

    # Checks that no invalid compilers are being used
    if ("fortran" in progs) and (not sinlis('gfortran', commands)):
        raise SyntaxError("Fortran must be compiled using gfortran")
    if ("c" in progs) and (not sinlis('gcc', commands)):
        raise SyntaxError("C must be compiled using gcc")
    if ("cPlusPlus" in progs) and (not sinlis('g++', commands)):
        raise SyntaxError("Fortran must be compiled using g++")
    
    cc1 = commands
    commands = extra_uset(commands, tempdir, boapp)

    # If there are changes, then the compile instructions is added
    if cc1 != commands:
        rcon += midsyn("USER_SETUP", "/work/compile_instructions.sh")

    # Error if there are no commands, i.e. : the user has only compiled
    if commands == []:
        raise SyntaxError("No commands have been submitted, only compile instructions")

    #User setup
    comproc(commands, tempdir, boapp)

    rcon += midsyn("COMMAND", "bash: exec.sh")

    # Output files
    for ofil in jdat["output_file"]:
        rcon += midsyn("OUTPUT", ofil)

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
        setfiles = dictdata["setup_filename"]
        outfiles = dictdata["output_file"]
        coms = dictdata["command_lines"]
        Username = dictdata["Username"]

    except:
        return "INVALID, json lacks at least one field"

    if  pp.token_test(TOK) == False:
        shutil.rmtree(TMP)
        return 'INVALID, invalid token'


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



    # MIDAS files are stored in a temporary folder
    boapp = "boinc2docker"
    TMP = "/tmp/"+tmp_dir+'/'

    # Creates directory if it does not exist
    if not os.path.isdir(TMP):
        os.makedirs(TMP)

    if 'README.txt' in os.listdir(TMP):
        return "INVALID, README.txt is a MIDAS reserved file. Please, remove it and try again"

    for file in os.listdir(TMP):

        if (file.split(".")[-1] == "tgz") or (".".join(file.split(".")[::-1][:2:][::-1]) == "tar.gz"):
            # Takes the contents out and deletes the tar
            try:
                tar = tarfile.open(TMP+file)
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

    # The application is volcon if using c++ libraries
    if libs['cPlusPlus'] != []:
        boapp = "volcon"

    # Creates an acceptable README
    with open(TMP+"README.txt", 'w') as readme:
        try:
            readme.write(verne(dictdata, TMP, boapp))
        except Exception as e:
            shutil.rmtree(TMP)
            return "INVALID, "+str(e)

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
    if (not mdr.install_libraries(TMP+'/README.txt')) and (mdr.install_libraries(TMP+'/README.txt') != []):
        shutil.rmtree(TMP)
        return 'INVALID, Language does not support libraries'

    # Moves the directory to MIDAS and processes it
    ALL_USER_DATA = os.listdir('/home/boincadm/project/api/sandbox_files/DIR_'+str(TOK))
    while True:
        new_MID = 'MID_'+pp.random_dir_name()
        if new_MID not in ALL_USER_DATA:
            break

    MIDAS_PATH = UPLOAD_FOLDER+'/DIR_'+str(TOK)+'/'+new_MID
    shutil.copytree(TMP, MIDAS_PATH)
    shutil.rmtree(TMP)

    # Adds the job to MySQL
    mints.add_MIDAS_job(Username, TOK, tags_used, new_MID, coms, boapp, "web", "MIDAS ready")

    return 'File submitted for processing'



if __name__ == '__main__':
    # Outside of container
    app.run(host = '0.0.0.0', port = 6075, debug=False, threaded=True)
