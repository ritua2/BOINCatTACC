"""
BASICS

Interactions with MySQL database
"""


import datetime
import mysql.connector as mysql_con
import os
import random
import redis
import time



r = redis.Redis(host = '0.0.0.0', port = 6389, db = 3)


# Returns the time format YYYY-MM-DD hh:mm:ss (UTC)
def timnow():
    return datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")



# Creates a temporary VolCon-ID tag in Redis
# The reason is that Redis rpop operations are atomic and so avoid race conditions
def tag_volcon(VID):
    r.rpush(VID, timnow())



# Checks if a value has not been checked yet
def race_condition_occurred(VID):
    if r.rpop(VID) == None:
        return True
    else:
        return False



# Adds a job to MySQL
# GPU (1 or 0)
# VID (str): Volcon ID
# public (1 or 0): Image is publicly available in Dockerhub, 0 for MIDAS
def add_job(token, image, commands, GPU, VID, priority_level, public=1):
    boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
    cursor = boinc_db.cursor(buffered=True)

    insert_new_job = (
        "INSERT INTO volcon_jobs (token, Image, Command, Date_Sub, Notified, status, GPU, volcon_id, priority, public) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

    cursor.execute(insert_new_job, (token, image, commands, timnow(), "0", "Received", GPU, VID, priority_level, public) )
    boinc_db.commit()
    cursor.close()
    boinc_db.close()



# Updates a certain VolCon ID with a new status
# Assumed to be non-locking
def update_job_status(VID, new_status, lock = False):

    if not lock:
        boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
        cursor = boinc_db.cursor(buffered=True)
        cursor.execute( "UPDATE volcon_jobs SET status = %s WHERE volcon_id = %s", (new_status, VID))
        boinc_db.commit()
        cursor.close()
        boinc_db.close()
    else:
        time.sleep(random.uniform(0, 0.030))
        boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
        cursor = boinc_db.cursor(buffered=True)
        cursor.execute("SELECT * FROM volcon_jobs WHERE volcon_id = '%s' FOR UPDATE NOWAIT", (VID))
        cursor.execute("UPDATE volcon_jobs SET status = %s WHERE volcon_id = %s", (new_status, VID))
        boinc_db.commit()
        cursor.close()
        boinc_db.close()




# Updates the mirror ip
def update_mirror_ip(VID, mirror_ip):
    boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
    cursor = boinc_db.cursor(buffered=True)
    cursor.execute( "UPDATE volcon_jobs SET mirror_ip = %s WHERE volcon_id = %s", (mirror_ip, VID))
    boinc_db.commit()
    cursor.close()
    boinc_db.close()



# Finds available jobs
# A job is defined as available if (ERROR == NULL) and (status == 'Mirror received files')
# Filters by GPU (1: GPU is required, 0: GPU is not required)
# Filters by priority level
# Returns a list of VolCon IDs

def available_jobs(GPU_required, priority_level, public=1):

    boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
    cursor = boinc_db.cursor(buffered=True)

    find_VIDS = ("SELECT volcon_id, mirror_ip FROM volcon_jobs WHERE (ERROR IS NULL AND status = 'Mirror received files') AND ((GPU <= %s AND priority = %s) AND public >= %s)")
    cursor.execute(find_VIDS, (GPU_required, priority_level, public) )

    V = []
    for vid in cursor:
        V.append([vid[0], vid[1]])
    cursor.close()
    boinc_db.close()
    return V



# Checks if a certian Volcon-ID exists
def VolCon_ID_exists(VID):
    boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
    cursor = boinc_db.cursor(buffered=True)
    cursor.execute("SELECT volcon_id FROM volcon_jobs WHERE volcon_id = %s", (VID,) )

    for ips in cursor:
        # Exists
        cursor.close()
        boinc_db.close()
        return True

    cursor.close()
    boinc_db.close()
    # Does not exist
    return False



# Updates a certain VolCon ID after receiving its results
def update_execution_report(VID, command_error, computation_time, date_run, download_time, Error, notification_email_status, client_ip):

    boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
    cursor = boinc_db.cursor(buffered=True)

    date_received = timnow()

    to_be_executed = ("UPDATE volcon_jobs SET status = %s, Command_Errors = %s, "+
                    "computation_time = %s, Date_Run = %s, download_time = %s, Error = %s, Notified = %s, "+
                    "received_time = %s, client_ip = %s    WHERE volcon_id = %s"
                    )

    cursor.execute( to_be_executed,
                    ("Complete", command_error, computation_time, date_run, download_time, Error, notification_email_status, date_received, client_ip, VID))
    boinc_db.commit()
    cursor.close()
    boinc_db.close()



# Updates the database with a failed job
def failed_execution_report(VID, date_run, download_time, Error, notification_email_status, client_ip):

    boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
    cursor = boinc_db.cursor(buffered=True)

    date_received = timnow()

    to_be_executed = ("UPDATE volcon_jobs SET status = %s, "+
                    "Date_Run = %s, download_time = %s, Error = %s, Notified = %s, "+
                    "received_time = %s, client_ip = %s    WHERE volcon_id = %s"
                    )

    cursor.execute( to_be_executed,
                    ("Failed", date_run, download_time, Error, notification_email_status, date_received, client_ip, VID))
    boinc_db.commit()
    cursor.close()
    boinc_db.close()



# Finds the Token associated with a  VolCon_ID
def token_from_VolCon_ID(VID):
    boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
    cursor = boinc_db.cursor(buffered=True)
    cursor.execute("SELECT Token FROM volcon_jobs WHERE volcon_id = %s", (VID,) )

    for ips in cursor:
        return ips[0]

    cursor.close()
    boinc_db.close()
    # Does not exist
    return False
