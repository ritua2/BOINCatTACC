#!/usr/bin/env python3

"""
BASICS

Sends a researcher an email when a job has been completed
Designed for the adtd-protocol in mind
"""


import redis
import datetime
import smtplib
import os, shutil, sys
from os.path import basename
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests



r = redis.Redis(host = '0.0.0.0', port = 6389, db = 0)

"""
Necessary functions
"""

# Obtains the email of a user provided a token
# toktok (str): Token
def obtain_email(toktok):
    
    toktok = toktok.replace('\n', '').replace(' ', '')
    with open("/home/boincadm/project/html/user/token_data/Tokens.txt", 'r') as TFIL:
         for line in TFIL:
             if toktok in line:
                return line.split(',')[-1].replace('\n', '').replace(' ', '')

# Obtains the names of all the files with a certain name in the Boinc database
# Includes the full path
# namnam (str): Name of the job
# YYYYMMDD (str): Date when the job was received, myst be in format YYYY-MM-DD
def job_result_files(namnam, YYYYMMDD):
    
    PPP = []
    MAIN_DIR = "/results/adtdp/"
    FULLPATH = MAIN_DIR+YYYYMMDD.split(" ")[0] + "/"

    try:
    
        for filfil in os.listdir(FULLPATH):
            if namnam in filfil:
                PPP.append(FULLPATH+"/"+str(filfil))
    except:
        return PPP
    return PPP   

# Emails an user 
# send_from (str): Sender name
# send_to (arr) (str): Email address of recipients
# text (str): Text to be sent, always constant
# files (arr) (str): Files to be included, add full path

def send_mail(send_from, send_to, subject, text, attachments):

    sender = os.environ['BOINC_EMAIL']
    gmail_password = os.environ['BOINC_EMAIL_PASSWORD']
    
    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = 'BOINC job completed'
    outer['To'] = ', '.join([send_to])
    outer['From'] = sender
    # Adds the text
    outer.attach(MIMEText(text))
    # Add the attachments to the message
    for file in attachments:
        with open(file, 'rb') as fp:
             msg = MIMEBase('application', "octet-stream")
             msg.set_payload(fp.read())
        encoders.encode_base64(msg)
        msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
        outer.attach(msg)

    composed = outer.as_string()

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(sender, gmail_password)
            s.sendmail(sender, [send_to], composed)
            s.close()

    except:
        print("Unable to send the email. Error: ", sys.exc_info()[0])
        raise

# Creates the main text submitted
# timrec (str): Time received
# Ocome (int): Outcome, 1 (Success), 3 (Computational Error)
# TOK (str): User token
# ATTA (arr) (str): Attachment files
def automatic_text(timrec, Ocome, TOK, ATTA):


    Text1 = "Your BOINC job has been completed with status: "+Ocome.upper()
    Text1 += ".\nAll results files, if any, are attached.\nServer received results on: "+timrec
    Text1 += " UTC. This message was sent on "+prestime+" UTC.\n\n"
    Text1 += "Your results are also available in your Reef account in the directory ___RESULTS.\n\n"
    Text1 += "Click or copy the following URLs to access your results:\n"
    for anat in ATTA:
        ST = os.environ["SERVER_IP"]+":5060/boincserver/v2/reef/results/"
        ST += TOK+"/"+anat.split("/")[-1]
        Text1 += ST+'\n'


    Text1 += "Sincerely,\n  TACC BOINC research group\n\n\n"
    Text1 += "NOTE: This is an automated message, all emails received at this address will be ignored."
    return Text1


"""
Main
"""

# Loops through all the Redis Error messages and notifications

allrun = r.llen('Token')

all_notified = [r.lindex('Notified', x).decode('UTF-8') for x in range(0, allrun)]

# Names of the the jobs submitted
all_names = [r.lindex('Error', y).decode('UTF-8') for y in range(0, allrun)]

prestime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Contains the names of jobs which have been completed and the user has not
# been notified yet:
# [ Result name, Outcome, Token, Time Received results ]
to_be_notified = [[], [], [], []]

# Finds which ones have already been finished
# Also updates the database to mark them as run
for idid in range(0, allrun):

    curname = all_names[idid]
    notif = all_notified[idid]

    # Skips already notified jobs
    if notif != '0':
        continue

    this_nam = all_names[idid]

    # Filters those not processed by adtdp
    if ('|' not in this_nam):
        continue

    # Parses through all the rest
    IDENTITY = this_nam.split("|")[0].replace(" ", "")
    OUTCOME = this_nam.split("|")[1].replace(" ", "")
    TOK = r.lindex("Token", idid).decode("UTF-8")
    TREC = r.lindex("Date (Run)", idid).decode("UTF-8")
    to_be_notified[0].append(IDENTITY)
    to_be_notified[1].append(OUTCOME)
    to_be_notified[2].append(TOK)
    to_be_notified[3].append(TREC)


    prestime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Marks the job as notified
    r.lset("Notified", idid, prestime)


# Sends the email with the links
# Moves the results to Reef so that they are accessible
for nvnv in range(0, len(to_be_notified[0])):

    attachments = job_result_files(to_be_notified[0][nvnv], to_be_notified[3][nvnv])
    email_text = automatic_text(to_be_notified[3][nvnv], to_be_notified[1][nvnv], to_be_notified[2][nvnv], attachments)
    researcher_email = obtain_email(to_be_notified[2][nvnv])
    print(researcher_email)
    # Adds the result to a Reef folder
    for resfil in attachments:
        requests.post('http://'+os.environ['Reef_IP']+':2001/reef/result_upload/'+os.environ['Reef_Key']+'/'+to_be_notified[2][nvnv], files={"file": open(resfil, "rb")})
    send_mail('Automated BOINC Notifications', researcher_email, 'Completed Job', email_text, attachments)
