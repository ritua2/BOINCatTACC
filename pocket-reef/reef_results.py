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


@app.route('/reef/results/<ukey>/<toktok>/<FIL>')
def results_file(ukey, toktok, FIL):

    if not bf.valid_key(ukey):
        return "INVALID key, cannot create a new user"
    if str('DIR_'+toktok) not in os.listdir(REEF_FOLDER):
       return 'User directory does not exist'

    USER_DIR = REEF_FOLDER+'DIR_'+str(toktok)+'/___RESULTS/'
    if str(FIL) not in os.listdir(USER_DIR):
       return 'File not available'

    return send_file(USER_DIR+str(FIL))


if __name__ == '__main__':
   app.run(host =='0.0.0.0', port = 801)
