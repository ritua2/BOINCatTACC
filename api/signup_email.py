#!/usr/bin/env python3

"""
BASICS

Sends an user an email when signing up
"""

import os
import smtplib
from flask import Flask
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



app = Flask(__name__)


# Designed for volunteer registration
@app.route("/boincserver/v2/api/signup/volunteer/<email>/<anonym>")
def signup_volunteer(email, anonym):

    sender = os.environ['BOINC_EMAIL']
    gmail_password = os.environ['BOINC_EMAIL_PASSWORD']

    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = 'BOINC sign-up'
    outer['To'] = email
    outer['From'] = sender

    text = "Welcome to TACC-2-BOINC,\n\nThank you for registering as a volunteer. "
    text += "If you have not done so, please install the BOINC client (http://boinc.berkeley.edu/download.php) and Virtualbox (https://www.virtualbox.org/wiki/Downloads).\n"
    text += "When prompted, select  "+os.environ['URL_BASE'].replace("http://", '')+"  as the BOINC project.\n"
    text += "\nFor GDPR compliance reasons, we have created an anonymized name for you and that is: "+anonym+" . This name is "
    text += "associated with your account and you can see it in your profile settings. This anonymized named will be displayed "
    text += "in the leaderboard on the TACC-2-BOINC website.\n"
    text += "\n\nSincerely,\n\nThe TACC development team"

    # Adds the text
    outer.attach(MIMEText(text))

    composed = outer.as_string()

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(sender, gmail_password)
            s.sendmail(sender, [email], composed)
            s.close()

            return "Email sent"

    except:
        return "INVALID, could not send email"


if __name__ == '__main__':
   app.run(host = '0.0.0.0', port = 6040)

