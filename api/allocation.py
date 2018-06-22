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

    # Sets up what to delete (more than one option may be selected):
    #     - all: Deletes all the data in Reef, including directories
    #     - basic: Deletes the temporary MIDAS directories, non-accessible to users in regular cases
    #     - ordinary: Deletes Reef documents
    #     - results: Deletes the results
    # Write y/Y/yes/YES to delete, all other commands will not delete

    delete_all = str(request.form['all']).lower()
    delete_basic = str(request.form['basic']).lower()
    delete_ordinary = str(request.form['ordinary']).lower()
    delete_results = str(request.form['results']).lower()
    user_commands = map(pp.y_parser, [delete_all, delete_basic, delete_ordinary, delete_results])

    # Avoids users who do not want to delete any data
    if all((not x) for x in user_commands):
        return "INVALID, no files have been marked for erasing"

    # Computes the starting user space
    used_space = pp.user_sandbox_size(str(toktok))/1073741824












if __name__ == '__main__':
   app.run(host = '0.0.0.0', port = 5052)
