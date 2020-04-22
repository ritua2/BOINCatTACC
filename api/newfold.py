#!/usr/bin/env python3

"""
BASICS

Creates a folder on demand on supported directories
"""


import os
from flask import Flask


app = Flask(__name__)


# New tmp folder
@app.route("/boincserver/mkdir/tmp/<nd>")
def mkdir_tmp(nd):

    try:
        os.makedirs("/tmp/"+nd)

        # Changes permissions to make it possible for the BOINC apache process to access this directory
        os.chown("/tmp/"+nd, 33, 33)

        return "Created new directory"
    except:
        return "Directory already exists"


if __name__ == '__main__':
    # Outside of container
    app.run(host = '0.0.0.0', port = 6055, debug=False, threaded=True)
