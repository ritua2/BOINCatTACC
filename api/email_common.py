"""
BASICS

Common email sending procedures
"""


import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import requests
import smtplib




# Emails an user using the development queue
# send_to (arr) (str): Email address of recipients
# text (str): Text to be sent, always constant
# attachments (arr) (str paths): Attachments to be included, defaults to empty

def send_mail_dev(send_to, subject, text, attachments):
    sender = os.environ['BOINC_EMAIL']
    password = os.environ['BOINC_EMAIL_PASSWORD']

    # Creates the actual message
    main_text = MIMEMultipart()
    main_text['Subject'] = subject
    main_text['To'] = send_to
    main_text['From'] = sender
    main_text.attach(MIMEText(text, 'plain'))

    # Add the attachments to the message
    for file in attachments:
        with open(file, 'rb') as fp:
             msg = MIMEBase('application', "octet-stream")
             msg.set_payload(fp.read())
        encoders.encode_base64(msg)
        msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
        main_text.attach(msg)

    full_message = main_text.as_string()

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
             s.starttls()
             s.login(sender, password)
             s.sendmail(sender, [send_to], full_message)
             s.close()
        return "Results have been emailed to "+send_to
    except:
        return "ERROR sending email"



# Sends complete email, accounting for production or development
def send_mail_complete(send_to, subject, text, attachments):

    if os.environ["dev_yn"] == "y":
        return send_mail_dev(send_to, subject, text, attachments)
    else:
        outer = {}
        outer["email_subject"] = subject
        outer["email_content"] = text
        outer["user_email"] = send_to
        outer["attachments"] = [atta.split("/")[-1] for atta in attachments]

        # Results are temporarily stored outside the container
        for file in attachments:
            #requests.post('http://'+os.environ['URL_BASE'].split('/')[-1]+':5021/emails/provide_file',
            #                files={"file": open(file,"rb")})
            requests.post('http://0.0.0.0:5021/emails/provide_file',
                            files={"file": open(file,"rb")})

        # Requests the message to be sent
        #requests.post('http://'+os.environ['URL_BASE'].split('/')[-1]+':5021/send_emails', json=outer)
        requests.post('http://0.0.0.0:5021/send_emails', json=outer)




# Finds the location of a file in the volcon directory starting at a certain date
# filename (str): Must not include full path
# YYYYMMDD_hhmmss (str): date when the job was received, in format YYYY-MM-DD hh:mm:ss
def obtain_file_received_at_date(filename, YYYYMMDD_hhmmss, results_path="/results/volcon/"):

    d1 = datetime.datetime.strptime(YYYYMMDD_hhmmss.split(' ')[0], "%Y-%m-%d")
    ndays = -1

    while True:
        ndays += 1
        d2 = d1 + datetime.timedelta(days=ndays)
        new_path = results_path + d2.strftime("%Y-%m-%d")
        if not os.path.isdir(new_path):
            break

        if filename in os.listdir(new_path):
            return [new_path+"/"+filename, True]

    # File does not exist
    return [None, False]


def automatic_text(timrec, outcome, TOK, ATTA):

    Text1 = "Your BOINC job has been completed with status: "+outcome
    Text1 += ".\nAll results files, if any, are attached.\nServer received results on: "+timrec
    Text1 += " UTC. This message was sent on "+timrec+" UTC.\n\n"
    if ATTA != []:

        Text1 += "Your results are also available in your Reef account in the directory ___RESULTS.\n\n"
        Text1 += "Click or copy the following URLs to access your results:\n"
        for anat in ATTA:
            ST = os.environ["SERVER_IP"]+":5060/boincserver/v2/reef/results/"
            ST += TOK+"/"+anat.split("/")[-1]
            Text1 += ST+'\n'
            Text1 += "NOTE: If the download does not automatically start from the above URL, use curl or wget to download the file. For example: curl -O "+ST+"\n"

    Text1 += "\n"

    Text1 += "Sincerely,\n  TACC BOINC research group\n\n\n"
    Text1 += "NOTE: This is an automated message, all emails received at this address will be ignored."
    return Text1
