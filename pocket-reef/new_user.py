#!/usr/bin/env python3

"""
BASICS

Creates a new user, specified by their token
If the user already exists, an error result is returned
"""

import os
from flask import Flask, request
import base_functions as bf

app = Flask(__name__)
REEF_FOLDER = os.environ['Reef_Path']+"/sandbox/"


# toktok (str): User token
@app.route("/reef/create_user/<toktok>/<rkey>")
def create_user(toktok, rkey):


    if not bf.valid_key(rkey):
        return "INVALID key, cannot create a new user"

    try:
        os.makedirs(REEF_FOLDER+'DIR_'+str(toktok))
        os.makedirs(REEF_FOLDER+'DIR_'+str(toktok)+'/___RESULTS')
        return "Reef cloud storage now available"
    except:
        return "User already has an account"


if __name__ == '__main__':
   app.run(host = '0.0.0.0', port = 2002)
