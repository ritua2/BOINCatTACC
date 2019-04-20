#!/usr/bin/env python3

"""
BASICS

Sends a researcher an email when a job has been completed
"""

import mysql.connector as mysql_con
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

boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')

cursor = boinc_db.cursor()

# Choose only those units that have been completed
query = ("SELECT name,  outcome, received_time FROM result WHERE (server_state='5' AND !( file_delete_state='0'))")

cursor.execute(query)
completed_names, outcomes, recdates = [[], [], []]

for (name, outcome, recidat) in cursor:
     completed_names.append(name)
     outcomes.append(outcome)
     recdates.append(recidat)



cursor.close()
boinc_db.close()


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
    MAIN_DIR = "/results/boinc2docker/"
    d1 = datetime.datetime.strptime(YYYYMMDD.split(' ')[0], "%Y-%m-%d")

    try:
        
        n = 0
        # Accounts for jobs received on different days
        while True:
            d2 = d1 + datetime.timedelta(days=n)
            d3 = d2.strftime("%Y-%m-%d")
            FULLPATH = MAIN_DIR+d3 + "/"
    
            for filfil in os.listdir(FULLPATH):
                if namnam in filfil:
                    PPP.append(FULLPATH+"/"+str(filfil))
                    return PPP

            n += 1

    except:
        return PPP
 


# Counts how many results are there for one WU ID
# Necessary because not all workunits have just 1 result
# Most have 2
# wunam (str): Semi-complete BOINC job name
def result_ID_from_WUID(wuman):

    HJK = 0
    for RRNN in completed_names:

       if wuman in RRNN:
          HJK +=1
    
    return HJK



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


"""
Main
"""

# Loops through all the Redis Error messages and notifications

allrun = r.llen('Token')

all_notified = [r.lindex('Notified', x).decode('UTF-8') for x in range(0, allrun)]

# Names of the the jobs submitted
all_names = [r.lindex('Error', y).decode('UTF-8').split('.')[0] for y in range(0, allrun)]

prestime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Contains the names of jobs which have been completed and the user has not
# been notified yet:
# [ Result name, Outcome, Token ]
to_be_notified = [[], [], [], []]

# User tokens
all_toks = []

# Finds which ones have already been finished
# Also updates the database to mark them as run
for idid in range(0, allrun):
     
    curname = all_names[idid]
    notif = all_notified[idid] 
    # Skips already notified jobs
    if notif != '0':
       continue

    # Number of results per WU
    results_WUID = result_ID_from_WUID(curname)
    # Skips WU with just 1 result, lacking output files
    if results_WUID < 2:
       continue
    

    for renam, outcome, recidat in zip(completed_names, outcomes, recdates):

        if (curname in renam):
            results_WUID -= 1
        # All results must have been received for the result to be valid
        if results_WUID == 0:
            all_toks.append(r.lindex('Token', idid).decode('UTF-8'))
            to_be_notified[0].append(curname)
            to_be_notified[1].append(outcome)
            to_be_notified[2].append(obtain_email(r.lindex('Token', idid).decode('UTF-8')))
            to_be_notified[3].append(datetime.datetime.utcfromtimestamp(int(recidat)).strftime('%Y-%m-%d %H:%M:%S'))
            # Adds the time of notification
            r.lset('Notified', idid, prestime)
            break


# Creates the main text submitted
# timrec (str): Time received
# Ocome (int): Outcome, 1 (Success), 3 (Computational Error)
# TOK (str): User token
# ATTA (arr) (str): Attachment files
def automatic_text(timrec, Ocome, TOK, ATTA):

    if str(Ocome) == '1':
       outcome = "SUCCESS"
    elif str(Ocome) == '3':
       outcome = "ERROR: COMPUTATIONAL ERROR"
    else:
       outcome = "UNKNOWN RESULT"

    Text1 = "Your BOINC job has been completed with status: "+outcome
    Text1 += ".\nIf there are any result files, they are attached.\nServer received results on: "+timrec
    Text1 += " UTC. This message was sent on "+prestime+" UTC.\n\n"
    #Text1 += "Your results are also available in your Reef account in the directory ___RESULTS.\n\n"
    Text1 += "Click on or copy the following URL/s to access your results from the browser:\n"
    for anat in ATTA:
        ST = os.environ["SERVER_IP"]+":5060/boincserver/v2/reef/results/"
        ST += TOK+"/"+anat.split("/")[-1]
        Text1 += ST+'\n'


    Text1 += "NOTE: If the download does not automatically start from the above URL, use curl or wget to download the file. For example: curl -O "+ST+" .\n\n"

    Text1 += "Sincerely,\n  TACC BOINC research group\n\n\n"
    Text1 += "NOTE: This is an automated message, all emails received at this address will be ignored."
    return Text1

# Sends the emails
for nvnv in range(0, len(to_be_notified[0])):

    attachments = job_result_files(to_be_notified[0][nvnv], to_be_notified[3][nvnv])
    email_text = automatic_text(to_be_notified[3][nvnv], to_be_notified[1][nvnv], all_toks[nvnv], attachments)
    researcher_email = to_be_notified[2][nvnv]
    print(researcher_email)
    # Uploads the result to the external Reef container
    for resfil in attachments:
        requests.post('http://'+os.environ['Reef_IP']+':2001/reef/result_upload/'+os.environ['Reef_Key']+'/'+all_toks[nvnv], files={"file": open(resfil, "rb")})

    send_mail('Automated BOINC Notifications', researcher_email, 'Completed Job', email_text, attachments)
