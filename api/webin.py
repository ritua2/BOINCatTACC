#!/usr/bin/env python3

"""
BASICS

Processes all commands submitted through the web interface and creates a file ready for BOINC processing
"""

import os, sys, shutil
from flask import Flask, request, jsonify, send_file
import preprocessing as pp
from werkzeug.utils import secure_filename
import redis



app = Flask(__name__)
ADTDP_FOLDER = "/root/project/adtd-protocol/process_files"
FINAL_FOLDER = "/root/project/html/user/token_data/process_files"
SERVER_IP = os.environ['SERVER_IP']


@app.route("/boincserver/v2/api/process_web_jobs", methods=['GET', 'POST'])
def process_web_jobs():

    if request.method != 'POST':
       return "INVALID, no data provided"  


    # Only for internal use, all other use will return an error
    if (request.remote_addr != '0.0.0.0') and (request.remote_addr != SERVER_IP):
        return "INVALID, API for internal use only"


if __name__ == '__main__':
   app.run(host = '0.0.0.0', port = 5096)
