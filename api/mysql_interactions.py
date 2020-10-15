"""
BASICS

Interactions with MySQL database
"""


import datetime
import mysql.connector as mysql_con
import os
import pytz
import random
import redis
import time



r = redis.Redis(host = '0.0.0.0', port = 6389, db = 3)


# Returns the time format YYYY-MM-DD hh:mm:ss (UTC)
def timnow():
    return convert_datetime_timezone(datetime.datetime.utcnow()).strftime("%Y-%m-%d %H:%M:%S.%f")



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



# Converts from timezone tz1 to timezone tz2
# Returns a datetime object
def convert_datetime_timezone(dt, tz1="UTC", tz2="America/Chicago"):
    
    # Dates not yet processed
    if dt == "0.0":
        return None

    tz1 = pytz.timezone(tz1)
    tz2 = pytz.timezone(tz2)

    if type(dt).__name__ == "str":
        dt = datetime.datetime.strptime(dt,"%Y-%m-%d %H:%M:%S.%f")
    elif type(dt).__name__ == "datetime":
        pass
    else:
        sys.exit("INVALID type, type(dt) = "+type(dt).__name__)

    dt = tz1.localize(dt)
    dt = dt.astimezone(tz2)

    return dt


# Adds a VolCon job to MySQL
# GPU (1 or 0)
# VID (str): Volcon ID
# public (1 or 0): Image is publicly available in Dockerhub, 0 for MIDAS
# tags (str): Tags associated with the job
def add_job(token, image, commands, GPU, VID, priority_level, public=1, tags="STEM", username=None, origin="web"):
    boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
    cursor = boinc_db.cursor(buffered=True)

    insert_new_job = (
        "INSERT INTO volcon_jobs (token, Image, Command, Date_Sub, Notified, status, GPU, volcon_id, priority, public, tags, username, origin) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

    cursor.execute(insert_new_job, (token, image, commands, timnow(), "0", "Received", GPU, VID, priority_level, public, tags, username, origin) )
    boinc_db.commit()
    cursor.close()
    boinc_db.close()

    # Tags the job so that it is discoverable by VolCon runners
    # Completely different from tags
    # Adds tag
    tag_volcon(VID)



# Sets an already submitted VolCon MIDAS job as ready for processing
def make_MIDAS_job_available(job_id, Image, Command, GPU, VID, priority_level, public=0):

    boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
    cursor = boinc_db.cursor(buffered=True)

    insert_new_job = "UPDATE volcon_jobs SET Image=%s, Command=%s, Notified=%s, status=%s, GPU=%s, volcon_id=%s, priority=%s, public=%s WHERE job_id=%s"

    cursor.execute(insert_new_job, (Image, Command, "0", "Received", GPU, VID, priority_level, public, job_id) )
    boinc_db.commit()
    cursor.close()
    boinc_db.close()

    # Tags the job so that it is discoverable by VolCon runners
    # Completely different from tags
    # Adds tag
    tag_volcon(VID)



# Sets an already submitted boinc2docker MIDAS job as ready for processing
def make_boinc2docker_MIDAS_job_available(job_id, Image, Command):

    boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
    cursor = boinc_db.cursor(buffered=True)

    insert_new_job = "UPDATE boinc2docker_jobs SET Image=%s, Command=%s, status=%s WHERE job_id=%s"

    cursor.execute(insert_new_job, (Image, Command, "Job submitted", job_id) )
    boinc_db.commit()
    cursor.close()
    boinc_db.close()



# Adds a boinc2docker job to MySQL
def add_boinc2docker_job(username, token, tags, Image, Command, boinc_application, origin, status):


    boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
    cursor = boinc_db.cursor(buffered=True)

    insert_new_job = (
        "INSERT INTO boinc2docker_jobs (username, token, tags, Image, Command, date_processed, boinc_application, origin, status) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")

    cursor.execute(insert_new_job, (username, token, tags, Image, Command, timnow(), boinc_application, origin, status) )
    boinc_db.commit()
    cursor.close()
    boinc_db.close()



# Adds a MIDAS job, boinc2docker or VolCon
def add_MIDAS_job(username, token, tags, MIDAS_ID, Command, boinc_application, origin, status="MIDAS ready"):

    boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
    cursor = boinc_db.cursor(buffered=True)

    if boinc_application == "boinc2docker":
        insert_new_job = (
            "INSERT INTO boinc2docker_jobs (username, token, tags, Image, Command, date_processed, boinc_application, origin, status, boinc_error) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

        cursor.execute(insert_new_job, (username, token, tags, "Custom", Command, timnow(), boinc_application, origin, status, MIDAS_ID) )
        boinc_db.commit()

    elif boinc_application == "volcon":
        insert_new_job = (
            "INSERT INTO volcon_jobs (username, token, Image, Command, Date_Sub, status, tags, origin, Error) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")

        cursor.execute(insert_new_job, (username, token, "CUSTOM", Command, timnow(), status, tags, origin, MIDAS_ID) )
        boinc_db.commit()

    cursor.close()
    boinc_db.close()



# Selects MIDAS jobs waiting for both boinc2docker and VolCon
# Returns [[job_id, token, MIDAS ID, boapp], ...]
def get_available_MIDAS_jobs():

    boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')

    cursor_boinc2docker = boinc_db.cursor(buffered=True)
    cursor_boinc2docker.execute( "SELECT job_id, token, boinc_error, boinc_application FROM boinc2docker_jobs WHERE status = 'MIDAS ready'")

    available_MIDAS_jobs = []
    for row in cursor_boinc2docker:
        available_MIDAS_jobs.append([row[0], row[1], row[2], row[3]])

    cursor_boinc2docker.close()


    cursor_boinc2docker = boinc_db.cursor(buffered=True)
    cursor_boinc2docker.execute( "SELECT job_id, token, Error FROM volcon_jobs WHERE status = 'MIDAS ready'")

    for row in cursor_boinc2docker:
        available_MIDAS_jobs.append([row[0], row[1], row[2], "volcon"])

    cursor_boinc2docker.close()

    boinc_db.close()

    return available_MIDAS_jobs



# Updates the apache results path location
def update_results_path_apache(VID, results_path_apache):
    boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
    cursor = boinc_db.cursor(buffered=True)
    cursor.execute( "UPDATE volcon_jobs SET results_path_apache = %s WHERE volcon_id = %s", (results_path_apache, VID))
    boinc_db.commit()
    cursor.close()
    boinc_db.close()



# Updates the status of a job
def update_job_status1(job_id, boapp, new_status):
    boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
    cursor = boinc_db.cursor(buffered=True)

    if boapp == "boinc2docker":
        cursor.execute( "UPDATE boinc2docker_jobs SET status = %s WHERE job_id = %s", (new_status, job_id))
        boinc_db.commit()

    elif boapp == "volcon":
        cursor.execute( "UPDATE volcon_jobs SET status = %s WHERE job_id = %s", (new_status, job_id))
        boinc_db.commit()

    cursor.close()
    boinc_db.close()



# Updates job status, notified time, and error
# Useful when there are errors in processing
# If the notified time is not provided, it takes it to be the current at CST
def update_job_status_notified(job_id, boapp, new_status, notified_date_provided=False, processing_error=None):

    if not notified_date_provided:
        notified_date_provided = timnow()


    boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
    cursor = boinc_db.cursor(buffered=True)

    if boapp == "boinc2docker":
        cursor.execute( "UPDATE boinc2docker_jobs SET status = %s, date_notified=%s, boinc_error=%s WHERE job_id = %s", (new_status, job_id, notified_date_provided, processing_error))
        boinc_db.commit()

    elif boapp == "volcon":
        cursor.execute( "UPDATE volcon_jobs SET status = %s, Notified=%s, Error=%s WHERE job_id = %s", (new_status, job_id, notified_date_provided, processing_error))
        boinc_db.commit()

    cursor.close()
    boinc_db.close()




# Reads the apache results path location
def read_results_path_apache(VID):
    boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
    cursor = boinc_db.cursor(buffered=True)
    cursor.execute( "SELECT results_path_apache FROM volcon_jobs WHERE volcon_id = %s", (VID,))

    local_paths = []
    for row in cursor:
        local_paths.append(row[0])

    cursor.close()
    boinc_db.close()

    return local_paths



# Updates the apache results path location
def update_results_path_reef(VID, results_path_reef):
    boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
    cursor = boinc_db.cursor(buffered=True)
    cursor.execute( "UPDATE volcon_jobs SET results_path_reef = %s WHERE volcon_id = %s", (results_path_reef, VID))
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



# Obtains a list of tokens for a given user
def user_tokens(username):

    token_list = []

    boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
    cursor = boinc_db.cursor(buffered=True)
    cursor.execute("SELECT token FROM researcher_users WHERE username = %s", (username,) )

    for possible_tokens in cursor:
        token_list.append(possible_tokens[0])

    cursor.close()
    boinc_db.close()

    return token_list



# DEPRECATED
# tags table no longer in use, tags are now stored as a column in the volcon_jobs and boinc2docker_jobs tables
# ------------------
# Adds tag
# All variables must be passed as either string or None
# boinc_application (str): As of now, only "boinc2docker" or "volcon"
# origin: "terminal" or "web" (web interface)
def add_tag(username, token, tags, Image, Command, boinc_application, origin):
    boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
    cursor = boinc_db.cursor(buffered=True)

    insert_new_job = (
        "INSERT INTO tags (username, token, tags, Image, Command, date_processed, boinc_application, origin) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

    cursor.execute(insert_new_job, (username, token, tags, Image, Command, timnow(), boinc_application, origin) )
    boinc_db.commit()
    cursor.close()
    boinc_db.close()
