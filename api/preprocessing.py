"""
BASICS

Necessary functions for API work
"""


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mysql.connector as mysql_con
import os, sys
import random
import smtplib




# Finds if the token is valid
def token_test(token):

    boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
    cursor = boinc_db.cursor(buffered=True)
    cursor.execute("SELECT username FROM researcher_users WHERE token = %s", (token,) )

    for ips in cursor:
        # Exists
        cursor.close()
        boinc_db.close()
        return True

    cursor.close()
    boinc_db.close()
    # Does not exist
    return False



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
    dirnam = ''
    for qq in range(0, 7):
        dirnam += random.choice(TTT)

    return dirnam


# Computes the size of an user's sandbox
# TOK (str): Token

def user_sandbox_size(TOK):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk('/home/boincadm/project/api/sandbox_files/DIR_'+TOK):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

# Emails an user
# send_to (arr) (str): Email address of recipients
# text (str): Text to be sent, always constant

def send_mail(send_to, subject, text):
    sender = os.environ['BOINC_EMAIL']
    password = os.environ['BOINC_EMAIL_PASSWORD']

    # Creates the actual message
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['To'] = send_to
    msg['From'] = sender
    msg.attach(MIMEText(text, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as s:
         s.starttls()
         s.login(sender, password)
         full_message = msg.as_string()
         s.sendmail(sender, [send_to], full_message)
         s.close()


# Obtains the email of a user provided a token
# toktok (str): Token
def obtain_email(toktok):
    
    boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
    cursor = boinc_db.cursor(buffered=True)
    cursor.execute("SELECT email FROM researcher_users WHERE token = %s", (toktok,) )

    for user_email in cursor:
        # Exists
        cursor.close()
        boinc_db.close()
        return user_email[0]

    cursor.close()
    boinc_db.close()
    # Does not exist
    return False


# Changes y/yes to True, all other to False
# usans (str): User-provided answer
def y_parser(usans):

    if (usans == 'y') or (usans == 'yes'):
        return True

    return False
    