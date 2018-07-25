#!/usr/bin/env python3

"""
BASICS

Returns a results file
Different port because of how common it is
"""

import os
from flask import Flask, send_file
import base_functions as bf

app = Flask(__name__)
REEF_FOLDER = os.environ['Reef_Path']+"/sandbox/"


# Returns a results file
@app.route('/reef/results/<rkey>/<toktok>/<FIL>')
def results_file(rkey, toktok, FIL):

    if not bf.valid_key(rkey):
        return "INVALID key"
    if str('DIR_'+toktok) not in os.listdir(REEF_FOLDER):
       return 'INVALID, User directory does not exist'

    USER_DIR = REEF_FOLDER+'DIR_'+str(toktok)+'/___RESULTS/'
    if str(FIL) not in os.listdir(USER_DIR):
       return 'INVALID, File not available'

    return send_file(USER_DIR+str(FIL))


# Returns a space-separated list of all files a user has in results
@app.route("/reef/results_all/<rkey>/<toktok>")
def reef_results_all(toktok, rkey):

    if not bf.valid_key(rkey):
        return "INVALID key, cannot create a new user"

    USER_DIR = REEF_FOLDER+'DIR_'+str(toktok)+'/___RESULTS'

    # Returns the results (space-separated)
    return ' '.join(os.listdir(USER_DIR))



if __name__ == '__main__':
   app.run(host ='0.0.0.0', port = 2001)
