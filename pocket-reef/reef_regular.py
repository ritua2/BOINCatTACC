#!/usr/bin/env python3

"""
BASICS

Returns user files or information about them
"""

import os, sys
from flask import Flask, request, jsonify, send_file
import base_functions as bf
from werkzeug.utils import secure_filename


app = Flask(__name__)
REEF_FOLDER = os.environ['Reef_Path']+"/sandbox/"


# Checks if reef cloud storage is available
@app.route('/reef/status')
def api_operational():
    return 'External Reef cloud storage is available'


if __name__ == '__main__':
   app.run(host =='0.0.0.0', port = 800)
