#!/usr/bin/env python3

"""
BASICS

Provides the user with information about their allocation.
Allows to delete their images and data, including results
"""

import redis
import os, shutil
from flask import Flask, request, jsonify
from werkzeug.datastructures import ImmutableMultiDict
import docker
import preprocessing as pp


client = docker.from_env()
r_alloc = redis.Redis(host = '0.0.0.0', port = 6389, db =2)
app = Flask(__name__)


@app.route("/boincserver/v2/api/allocation_active")
def allocation_active():

    return "Allocation APIs are active"


# Checks if the user has enough space available in their allocation to do any processing
# Only returns, y/n
@app.route("/boincserver/v2/api/simple_allocation_check", methods = ['GET', 'POST'])
def simple_allocation_check():

    if request.method != 'POST':
        return "INVALID, no data provided"

    if request.form['token'] == '':
        return "INVALID, no token provided"

    toktok = request.form["token"]
    if pp.token_test(toktok) == False:
       return 'INVALID token'

    assigned_allocation = float(r_alloc.get(toktok).decode('UTF-8'))

    if assigned_allocation > 0:
        return 'y'

    return 'n'



# Allows the user to see how much space is still available in his allocation
# Allows to check the user's allocation status
@app.route('/boincserver/v2/api/allocation_status', methods = ['GET', 'POST'])
def allocation_status():

    if request.method != 'POST':
        return "INVALID, no data provided"

    if request.form['token'] == '':
        return "INVALID, no token provided"

    toktok = request.form["token"]

    if pp.token_test(toktok) == False:
       return 'Invalid token'

    used_space = pp.user_sandbox_size(str(toktok))/1073741824
    assigned_allocation = r_alloc.get(toktok).decode('UTF-8')
    all_info = {'Max. allocation': assigned_allocation+' GB',
                'Used space': str(used_space)+' GB', 
                'Space available left': str((1 - used_space/float(assigned_allocation))*100)+'% allocation available'}

    return jsonify(all_info)


# Deletes the user's data in Reef according to a specification
# Also useful for resetting the user's allocation to what it is supposed to be
# Designed for large scale deletes, not small ones
# Returns the amount of space cleared and the new available space
@app.route("/boincserver/v2/api/delete_user_data", methods = ['GET', 'POST'])
def delete_user_data():

    if request.method != 'POST':
        return "INVALID, no data provided"
    if request.form['token'] == '':
        return "INVALID, no token provided"

    toktok = request.form["token"]

    if pp.token_test(toktok) == False:
        return "Invalid token"

    # All of the options must be selected with either y, or left blank
    # Sets up what to delete (more than one option may be selected):
    #     - all: Deletes all the data in Reef, including directories
    #     - basic: Deletes the temporary MIDAS directories, non-accessible to users in regular cases
    #     - ordinary: Deletes Reef documents, not results, or MIDAS
    #     - results: Deletes the results
    # Write y/Y/yes/YES to delete, all other commands will not delete

    delete_all = str(request.form['all']).lower()
    delete_basic = str(request.form['basic']).lower()
    delete_ordinary = str(request.form['ordinary']).lower()
    delete_results = str(request.form['results']).lower()
    user_commands = list(map(pp.y_parser, [delete_all, delete_basic, delete_ordinary, delete_results]))

    # Avoids users who do not want to delete any data
    if all((not x) for x in user_commands):
        return "INVALID, no files have been marked for erasing"

    # Computes the starting user space
    used_space = pp.user_sandbox_size(str(toktok))/1073741824

    # Finds all the user data
    USER_PATH = "/home/boincadm/project/api/sandbox_files/DIR_"+toktok
    user_files = os.listdir(USER_PATH)

    if user_commands[0]:
        # Calls all delete options
        user_commands = [True, True, True, True]    

    if user_commands[1]:
        # Deletes all MIDAS directories
        ALL_MIDAS = [USER_PATH+'/'+x for x in user_files if x[:4:]=="MID_"]
        for y in ALL_MIDAS:
            shutil.rmtree(y)

    if user_commands[2]:
        # Deletes regular user files
        REGULAR_REEF = [USER_PATH+'/'+x for x in user_files if (not os.path.isdir(USER_PATH+'/'+x))]
        for z in REGULAR_REEF:
            os.remove(z)

    if user_commands[3]:
        # Deletes the results
        RESULTS = os.listdir(USER_PATH+"/___RESULTS")
        for w in RESULTS:
            os.remove(USER_PATH+"/___RESULTS/"+w)


    # Computes the saved space
    now_space = pp.user_sandbox_size(str(toktok))/1073741824
    recovered_space = used_space - now_space
    r_alloc.incrbyfloat(toktok, recovered_space)
    new_alloc = r_alloc.get(toktok).decode("UTF-8")

    return "Space recovered: "+str(recovered_space)+" GB; new allocated space: "+str(new_alloc)+" GB"


if __name__ == '__main__':
   app.run(host = '0.0.0.0', port = 5052, debug=False, threaded=True)
