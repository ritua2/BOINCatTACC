"""
BASICS

Necessary functions for API work
"""

import random
import os, sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import redis


r_val = redis.Redis(host = '0.0.0.0', port = 6389, db=2)



# Finds if the token is valid
def token_test(token):

   if r_val.get(token) is None:
      return False

   return True


# Creates a random file name with 18 characters

def random_file_name():

    HHH = 'abcdefghijklmnopqrstuvwxyz1234567890'
    fnam = "auk"
    for qq in range(0, 12):
        fnam += random.choice(HHH)
    else:
        fnam += ".txt"
    return fnam


# Creates a random directory name for MIDAS use
# All directories are 11 characters long

def random_dir_name():

    TTT = 'abcdefghijklmnopqrstuvwxyz1234567890'
    dirnam = 'dir-'
    for qq in range(0, 7):
        dirnam += random.choice(HHH)

    return fnam


# Computes the size of an user's sandbox
# TOK (str): Token

def user_sandbox_size(TOK):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk('/root/project/api/sandbox_files/DIR_'+TOK):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

# Emails an user
# send_to (arr) (str): Email address of recipients
# text (str): Text to be sent, always constant

def send_mail(send_to, subject, text):
    sender = os.environ['BOINC_EMAIL']
    gmail_password = os.environ['BOINC_EMAIL_PASSWORD']

    # Creates the actual message
    msg = MIMEMultipart()
    msg['Subject'] = 'Temporal token'
    msg['To'] = send_to
    msg['From'] = sender
    msg.attach(MIMEText(text, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as s:
         s.starttls()
         s.login(sender, password)
         full_message = msg.as_string()
         s.sendmail(sender, send_to, full_message)
         s.close()
