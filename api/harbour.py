#!/usr/bin/env python3


"""
BASICS

Creates an automated dockerfile for BOINC jobs. If the build fails, submits an email to the user with the error logs.
All images are named {TOKEN}:{10 letters sha256 hash}.
If the build succeeds, then the memory it occupies is reduced from the user's account
"""



import os, sys
import docker
import redis
import hashlib
import datetime
from midas_processing import midas_reader as mdr
import preprocessing as pp



r = redis.Redis(host = '0.0.0.0', port = 6389, db = 2)
# Starts a client for docker
client = docker.from_env()
image = client.images


Success_Message = "Your MIDAS job has generated an image submitted for processing.\nThis message was completed on DATETIME."
Failure_Message = "Your MIDAS job has failed dockerfile construction.\nThis message was sent on DATETIME."

# Creates a new docker image
# Designed so that it is easy to silence for further testing

# IMTAG (str): tag for the image
# FILES_PATH (str): Path to the files, most likely it will be the current directory
def user_image(IMTAG, FILES_PATH = '.'):

    image.build(path=FILES_PATH, tag=IMTAG.lower())


# Full process of building a docker image
def complete_build(IMTAG, FILES_PATH='.'):

    researcher_email = pp.obtain_email(IMTAG.split(':')[0])
    try:
        # image.build(IMTAG)
        MESSAGE = Success_Message.replace("DATETIME", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        pp.send_mail(researcher_email, 'Succesful MIDAS build', MESSAGE)
    except:
        MESSAGE = Failure_Message.replace("DATETIME", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        pp.send_mail(researcher_email, 'Failed MIDAS build', MESSAGE)


to_be_processed = [] # [[TOKEN, MIDAS directory], ...]

# Finds all the submitted jobs
for possible in r.keys():
    kim = possible.decode('UTF-8')
    if '.' in kim:
        to_be_processed.append([kim.split('.')[0], kim.split('.')[1]])
else:
    if len(to_be_processed) == 0:
        # No new user files to be processed
        sys.exit()



# Goes one by one in the list of submitted files
for HJK in to_be_processed:

    user_tok, dir_midas = HJK
    FILE_LOCATION = "/root/project/api/sandbox_files/DIR_"+user_tok+'/'+dir_midas

    # Goes to the file location
    os.chdir(FILE_LOCATION)
    #hti: how to install
    hti_OS = mdr.install_OS('README.txt')
    hti_langs =[mdr.install_language(y, mdr.valid_OS('README.txt')) for y in mdr.valid_language('README.txt')]
    hti_setup = mdr.user_guided_setup('README.txt')
    hti_libs = mdr.install_libraries('README.txt')

    # Obtains the commands to run
    ALL_COMS = mdr.present_input_files('.')
    FINAL_COMMANDS = []
    for acom in ALL_COMS:
        # C++ is special because it requires some dependecies to be set-up
        if 'c++' in acom[0].lower():
            pass

        # Other languages
        FINAL_COMMANDS.append(mdr.execute_command(acom))


    # All dockerfiles are named the same way {TOKEN}:{10 char hash}
    DTAG = user_tok+':'+hashlib.sha256(str(datetime.datetime.now()).encode('UTF-8')).hexdigest()[:10:]

    # Composes the dockerfile
    duck = hti_OS+"\n\n\n"+"\n".join(mdr.copy_files_to_image('.'))
    for inst_set in [hti_langs, hti_setup, hti_libs]:
        if inst_set == []:
            continue
        duck += "\nRUN "+" && ".join(inst_set)


    duck += "\n\nWORKDIR /work"

    # Actual command
    BOINC_COMMAND = DTAG+" /bin/bash -c  \"cd /work; "+"; ".join(FINAL_COMMANDS)+"; python3 /Mov_Specific.py\""
    complete_build(DTAG)



