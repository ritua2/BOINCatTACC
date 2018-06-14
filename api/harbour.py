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
    hti_langs =[mdr.install_language(y) for y in mdr.valid_language('README.txt')]


    # Obtains the commands to run
    ALL_COMS = mdr.present_input_files('.')
    FINAL_COMMANDS = []
    for acom in ALL_COMS:
        # C++ is special because it requires some dependecies to be set-up
        if 'c++' in acom[0].lower():
            pass

        # Other languages
        FINAL_COMMANDS.append(mdr.execute_command(acom))
