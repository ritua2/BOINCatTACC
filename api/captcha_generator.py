#!/usr/bin/env python3

"""
BASICS

Cloud storage of files on the BOINC server for using local files
"""

import base64
import os
from flask import Flask, send_file, after_this_request
import re
import requests

from captcha.image import ImageCaptcha




app = Flask(__name__)


# Request of job information for a TACC image job
# Returns a json object with the information
# Then deletes the directory to save space
@app.route("/boincserver/v2/api/request_captcha/<captcha_id>", methods=['GET'])
def request_captcha(captcha_id):

    # Checks if alphanumeric (a-z, A-Z, 0-9)
    if not bool(re.match("^[a-zA-Z0-9]+$", captcha_id)):
        return "INVALID, 'captcha_id' provided is not alphanumeric: (a-z, A-Z, 0-9)"

    image = ImageCaptcha()
    tmp_captcha_file = "/tmp/"+captcha_id+".png"
    image.write(captcha_id, tmp_captcha_file)


    @after_this_request
    def remove_files(response):
        os.remove(tmp_captcha_file)
        return response

    return base64.b64encode(open(tmp_captcha_file, "rb").read())



if __name__ == '__main__':
    # Unaccessible outside the container
    app.run(host ='0.0.0.0', port = 6051, debug=False, threaded=True)
