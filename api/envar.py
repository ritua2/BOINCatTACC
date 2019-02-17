#!/usr/bin/env python3

"""
BASICS

Returns some environmental variables
In a port outside the VM
"""


from flask import Flask, jsonify
import os


app = Flask(__name__)


# Returns the Reef environmental variables
@app.route("/boincserver/v2/api/env/reef")
def reef():

    return jsonify({"Reef_IP":os.environ['Reef_IP'], "Reef_Key":os.environ['Reef_Key']})




if __name__ == '__main__':
   app.run(host = '0.0.0.0', port = 6071, debug=False, threaded=True)
