"""
BASICS

Reads the MySQL database and submits the jobs that have not been done yet to
the boinc2docker application
"""

import datetime
import mysql.connector as mysql_con
import os
import pytz
import subprocess as sp



# Returns the UTC datetime (UTC)
def timnow_dt():
    return datetime.datetime.utcnow()


# Converts from timezone tz1 to timezone tz2
# Returns a datetime object
def convert_datetime_timezone(dt):
    
    UTC_tz = pytz.timezone("UTC")
    dt1 = UTC_tz.localize(dt)

    dt1 = dt1.astimezone(pytz.timezone("America/Chicago"))
    return dt1


# Finds all jobs that are waiting to be run
boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
cursor = boinc_db.cursor(buffered=True)

find_not_run = ("SELECT job_id, Image, Command FROM boinc2docker_jobs WHERE status='Job submitted'")
cursor.execute(find_not_run)

left_to_run = []
for job_id, Image, Command in cursor:
    left_to_run.append([job_id, Image, Command])
cursor.close()
boinc_db.close()



# Runs the job and updates the status
for a_job_id, an_image, several_commands in left_to_run:

    prestime = convert_datetime_timezone(timnow_dt())

    full_command = "/home/boincadm/project/bin/boinc2docker_create_work.py "+an_image+" "+several_commands

    jobsub = sp.Popen(full_command, shell = True, stdout = sp.PIPE)

    streaming = jobsub.communicate()[0].decode('UTF-8')

    BOINC_output = streaming.replace("\n", "").split(' ')[-1]

    # Updates date and error message
    boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
    cursor = boinc_db.cursor(buffered=True)
    cursor.execute("UPDATE boinc2docker_jobs SET date_run = %s, boinc_error = %s, status = 'Job run'  WHERE job_id = %s", (prestime, BOINC_output, a_job_id))
    boinc_db.commit()
    cursor.close()
    boinc_db.close()
