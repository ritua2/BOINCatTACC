#!/usr/bin/env python3

"""
BASICS

Provides the framework to assign tokens based on a 2 factor authorization
"""


from flask import Flask, request
import hashlib
import json
import mysql.connector as mysql_con
import os
import preprocessing as pp
import random
import requests
from werkzeug.datastructures import ImmutableMultiDict



app = Flask(__name__)




# Registers an user if they come from TACC or any other allowed organization
# No email authorization required
# If they are already registered, then they simply run the job
@app.route("/boincserver/v2/api/authorize_from_org", methods = ['GET', 'POST'])
def authorize_from_org():

    if request.method != "POST":
        return "INVALID, no data provided"

    EMAIL = request.form["email"]
    ORG_KEY = hashlib.sha256(request.form["org_key"].encode('UTF-8')).hexdigest()
    USERNAME = request.form["username"]


    if EMAIL=='':
        return "INVALID, email was not provided"


    boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
    cursor = boinc_db.cursor(buffered=True)
    cursor.execute("SELECT org_name FROM organizations WHERE org_key = %s", (ORG_KEY,) )

    for org_name in cursor:
        cursor.close()
        boinc_db.close()
        selected_org = org_name[0]
        break
    else:
        cursor.close()
        boinc_db.close()
        # Does not exist
        return "INVALID, user organization is not registered"


    # Returns the token of an user if it exists
    boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
    cursor = boinc_db.cursor(buffered=True)
    cursor.execute("SELECT token FROM researcher_users WHERE email=%s AND organization=%s AND username=%s", (EMAIL, selected_org, USERNAME) )

    for user_tok in cursor:
        cursor.close()
        boinc_db.close()
        return user_tok[0]

    cursor.close()
    boinc_db.close()


    # Adds user if it does not exist already
    user_tok = EMAIL

    boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
    cursor = boinc_db.cursor(buffered=True)
    cursor.execute("INSERT INTO researcher_users (token, email, username, organization) VALUES (%s, %s, %s, %s)", (user_tok, EMAIL, USERNAME, selected_org) )
    boinc_db.commit()
    cursor.close()
    boinc_db.close()


    # Checks if the email directory exists
    if not os.path.exists("/home/boincadm/project/api/sandbox_files/DIR_"+user_tok):
        # Also creates a Reef directory
        requests.get('http://'+os.environ['Reef_IP']+':2002/reef/create_user/'+user_tok+'/'+os.environ['Reef_Key'])

        # Creates also the local directories for MIDAS usage
        os.mkdir("/home/boincadm/project/api/sandbox_files/DIR_"+user_tok)
        os.mkdir("/home/boincadm/project/api/sandbox_files/DIR_"+user_tok+'/___RESULTS')

    return user_tok




if __name__ == '__main__':
   app.run(host = '0.0.0.0', port = 5054, debug=False, threaded=True)
