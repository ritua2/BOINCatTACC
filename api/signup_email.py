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

    text = "Welcome to BOINC@TACC,\n\nThank you for registering as a volunteer! "
    text += "If you have not done so, please install the BOINC client (http://boinc.berkeley.edu/download.php) and Virtualbox (https://www.virtualbox.org/wiki/Downloads) to run BOINC@TACC jobs. "
    text += "When prompted, select BOINC@TACC from the project list or manually add the following URL: "+os.environ['URL_BASE'].replace("http://", '')+" .\n"
    text += "\nFor GDPR compliance reasons, we have created an anonymized name for you and that is: "+anonym+" . This name is "
    text += "associated with your account and you can see it in your profile settings. This anonymized named will be displayed "
    text += "in the leaderboard on the BOINC@TACC website.For getting your actual screen name and not the anonymized name displayed on the leaderboard, "
    text += "change it from "+os.environ['URL_BASE'].replace("http://", "https://")+"/home.php .\n"
    text += "\n\nSincerely,\n\nThe TACC development team"

    # Send the email
    return ec.send_mail_complete(email, 'BOINC sign-up', text, [])



# Sends an email with links so that users can validate their email
@app.route("/boincserver/v2/api/validate_email/volunteer/<email>/<validate_key>")
def validate_email(email, validate_key):

    text = "Welcome to BOINC@TACC,\n\nThank you for registering as a volunteer!\n\n"
    text += "Please verify your email by clicking or copying the following link into your browser search bar: "
    text += os.environ['URL_BASE'].replace("http://", "https://")+"/validate_email.php?email_addr="+email+"&validate_key="+validate_key
    text += "\n\nSincerely,\n\nThe TACC development team"

    # Send the email
    return ec.send_mail_complete(email, 'BOINC email verification', text, [])


if __name__ == '__main__':
   app.run(host = '0.0.0.0', port = 6040, debug=False, threaded=True)

