#!/usr/bin/env python3

"""
BASICS

Sends an user an email when signing up
"""

import email_common as ec
from flask import Flask
import os
import requests


app = Flask(__name__)


# Designed for volunteer registration
@app.route("/boincserver/v2/api/signup/volunteer/<email>/<anonym>")
def signup_volunteer(email, anonym):

    # Create the enclosing (outer) message
    outer = {}
    outer['email_subject'] = 'BOINC sign-up'
    outer['user_email'] = email

    text = "Welcome to BOINC@TACC,\n\nThank you for registering as a volunteer! "
    text += "If you have not done so, please install the BOINC client (http://boinc.berkeley.edu/download.php) and Virtualbox (https://www.virtualbox.org/wiki/Downloads) to run BOINC@TACC jobs. "
    text += "When prompted, select BOINC@TACC from the project list or manually add the following URL: "+os.environ['URL_BASE'].replace("http://", '')+" .\n"
    text += "\nFor GDPR compliance reasons, we have created an anonymized name for you and that is: "+anonym+" . This name is "
    text += "associated with your account and you can see it in your profile settings. This anonymized named will be displayed "
    text += "in the leaderboard on the BOINC@TACC website.For getting your actual screen name and not the anonymized name displayed on the leaderboard, please send an email to rauta@tacc.utexas.edu.\n"
    text += "\n\nSincerely,\n\nThe TACC development team"

    # Adds the text
    outer["email_content"] = text

    # Send the email
    return ec.send_mail_complete(email, 'BOINC sign-up', text, [])



if __name__ == '__main__':
   app.run(host = '0.0.0.0', port = 6040, debug=False, threaded=True)

