#!/usr/bin/env python3

"""
BASICS

Sends a researcher an email when a job has been completed
"""


import datetime
import glob
import mysql.connector as mysql_con
import os, shutil, sys
from os.path import basename
import pytz
import requests
import  tarfile

from api import email_common as ec



# Converts from timezone UTC to timezone America/Chicago
# Returns a datetime object
def convert_datetime_timezone(dt, original_timezone="UTC", final_timezone="America/Chicago"):

    original_tz_object = pytz.timezone(original_timezone)
    dt1 = original_tz_object.localize(dt)

    dt1 = dt1.astimezone(pytz.timezone(final_timezone))
    return dt1



# Returns the Unix timestamp of a datetime object in the specified timezone
def datetime_to_timestamp(dt, original_timezone, final_timezone):

    original_tz_object = pytz.timezone(original_timezone)
    dt1 = original_tz_object.localize(dt)

    dt1 = dt1.astimezone(pytz.timezone(final_timezone))

    return dt1.timestamp()



# Goes through the submitted jobs by researchers
boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1],
                            port = 3306, user = os.environ["MYSQL_USER"],
                            password = os.environ["MYSQL_UPASS"],
                            database = 'boincserver')
cursor = boinc_db.cursor()

# Choose only those units that have been completed
query = ("SELECT job_id, username, token, date_processed, status, boinc_error FROM boinc2docker_jobs WHERE date_notified IS NULL AND status='Job run'")
cursor.execute(query)

pending_jobs_to_be_notified = [[], [], [], [], [], []]

for (job_id, username, token, date_processed, status, boinc_error) in cursor:
    pending_jobs_to_be_notified[0].append(job_id)
    pending_jobs_to_be_notified[1].append(username)
    pending_jobs_to_be_notified[2].append(token)
    pending_jobs_to_be_notified[3].append(date_processed)
    pending_jobs_to_be_notified[4].append(status)
    pending_jobs_to_be_notified[5].append(boinc_error)

cursor.close()
boinc_db.close()


if len(pending_jobs_to_be_notified[3]) == 0:
    print("No jobs pending notification")
    sys.exit()


first_submitted_job_datetime= min(pending_jobs_to_be_notified[3])
first_submitted_job_UTC_unix_timestamp = datetime_to_timestamp(first_submitted_job_datetime, "America/Chicago", "UTC")


# Selects the corresponding jobs processed by the BOINC scheduler
boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1],
                            port = 3306, user = os.environ["MYSQL_USER"],
                            password = os.environ["MYSQL_UPASS"],
                            database = 'boincserver')
cursor = boinc_db.cursor()

query = ("SELECT name,  outcome, received_time FROM result WHERE (server_state='5' AND !( file_delete_state='0') AND received_time >= %s) GROUP BY workunitid")
cursor.execute(query, (first_submitted_job_UTC_unix_timestamp,))


# Keeps track of processed BOINC names
processed_boinc_names = {}


for (name, outcome, recidat) in cursor:

    name_without_ending = "_".join(name.split("_")[:3])
    processed_boinc_names[name_without_ending] = {"name":name, "outcome":outcome, "received_unix_UTC":recidat}

cursor.close()
boinc_db.close()





# Obtains the email of a user provided a token
# token (str): Token
def obtain_email(token):
    return token



# Computes the datetime (str) YYYY-MM-DD, no timezone specified, from a unix timestamp
def YYYY_MM_DD_from_unix(ts_unix):
    return datetime.datetime.utcfromtimestamp(ts_unix).strftime("%Y-%m-%d")


# Obtains the names of all the files with a certain name in the BOINC database
# Includes the full path
# job_name (str): Name of the job
# YYYY_MM_DD (str): Date when the job was received, myst be in format YYYY-MM-DD
def job_result_files(job_name, YYYY_MM_DD):

    PPP = []
    MAIN_DIR = "/results/boinc2docker/"+YYYY_MM_DD+"/"

    return glob.glob("/results/boinc2docker/"+YYYY_MM_DD+"/"+job_name+"*")



# Uploads a file to Reef
def upload_file_to_Reef(local_full_filepath, user_token):
    requests.post('http://'+os.environ['Reef_IP']+':2001/reef/result_upload/'+os.environ['Reef_Key']+'/'+user_token,
                    files={"file": open(local_full_filepath, "rb")})



# Finds the contents of a tar file
# full_path_to_tar (str): Full path to the tar file
def tar_contents(full_path_to_tar):

    tar = tarfile.open(full_path_to_tar)
    tar_contents = tar.getmembers()
    tar.close()
    return tar_contents



# Creates the main text submitted
# timrec (str): Time received (YYYY-MM-DD hh:mm:ss)
# prestime (str): Current time (YYYY-MM-DD hh:mm:ss)
# job_outcome (int): Outcome, 1 (Success), 3 (Computational Error)
# user_token (str): User token
# attachment_files (arr) (str): Attachment files
def automatic_text(timrec, prestime, job_outcome, user_token, attachment_files):

    if str(job_outcome) == '1':
       outcome = "SUCCESS"
    elif str(job_outcome) == '3':
       outcome = "ERROR: COMPUTATIONAL ERROR"
    else:
       outcome = "UNKNOWN RESULT"

    Text1 = "Your BOINC job has been completed with status: "+outcome
    Text1 += ".\nIf there are any result files, they are attached.\nServer received results on: "+timrec
    Text1 += " CST. This message was sent on "+prestime+" CST.\n\n"
    #Text1 += "Your results are also available in your Reef account in the directory ___RESULTS.\n\n"

    if (len(attachment_files) > 0) and any(len(tar_contents(result_file)) > 0 for result_file in attachment_files):
        Text1 += "Click on or copy the following URL/s to access your results from the browser:\n"
        for anat in attachment_files:
            ST = os.environ["SERVER_IP"]+":5060/boincserver/v2/reef/results/"
            ST += user_token+"/"+anat.split("/")[-1]
            Text1 += ST+'\n'


        Text1 += "NOTE: If the download does not automatically start from the above URL, use curl or wget to download the file. For example: curl -O "+ST+" .\n\n"
    elif all(len(tar_contents(result_file)) == 0 for result_file in attachment_files):
        Text1 += "The job ran normally without errors, however, no results have been uploaded to the server.\nThis reflects a possible error in the provided commands to be executed\n\n"


    Text1 += "Sincerely,\n  TACC BOINC research group\n\n\n"
    Text1 += "NOTE: This is an automated message, all emails received at this address will be ignored."
    return Text1




# Processes the jobs received
for nvnv in range(0, len(pending_jobs_to_be_notified[0])):

    boinc_name = pending_jobs_to_be_notified[5][nvnv]
    user_token = pending_jobs_to_be_notified[2][nvnv]
    job_id = pending_jobs_to_be_notified[0][nvnv]

    if boinc_name not in processed_boinc_names:
        continue

    job_outcome = processed_boinc_names[boinc_name]["outcome"]
    server_received_time_UTC = datetime.datetime.utcfromtimestamp(processed_boinc_names[boinc_name]["received_unix_UTC"])
    server_received_time_CST_str = convert_datetime_timezone(server_received_time_UTC, "UTC", "America/Chicago").strftime("%Y-%m-%d %H:%M:%S")


    current_time = convert_datetime_timezone(datetime.datetime.utcnow(), original_timezone="UTC", final_timezone="America/Chicago")
    current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")

    output_files_from_job = job_result_files(boinc_name, YYYY_MM_DD_from_unix(processed_boinc_names[boinc_name]["received_unix_UTC"]))
    researcher_email = obtain_email(user_token)

    # Ignores empty attachments
    real_outputs = [possible_result for possible_result in output_files_from_job if len(tar_contents(possible_result)) > 0]

    for an_output in real_outputs:
        upload_file_to_Reef(an_output, user_token)

    email_text = automatic_text(server_received_time_CST_str, current_time_str, job_outcome, user_token, real_outputs)
    ec.send_mail_complete(researcher_email, 'Completed BOINC Job', email_text, real_outputs)

    # Updates MySQL
    boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1],
                                port = 3306, user = os.environ["MYSQL_USER"],
                                password = os.environ["MYSQL_UPASS"],
                                database = 'boincserver')
    cursor = boinc_db.cursor()

    query = ("UPDATE boinc2docker_jobs SET status=%s, date_notified=%s WHERE job_id = %s")
    cursor.execute(query, ("Complete", current_time, job_id))
    boinc_db.commit()
    cursor.close()
    boinc_db.close()
