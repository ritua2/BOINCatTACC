"""
BASICS

Interactions with MySQL database
"""


import datetime
import mysql.connector as mysql_con
import os
import redis



r = redis.Redis(host = '0.0.0.0', port = 6389, db = 3)


# Returns the time format YYYY-MM-DD hh:mm:ss (UTC)
def timnow():
    return datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")



# Adds a job to MySQL
# GPU (1 or 0)
# VID (str): Volcon ID
def add_job(token, image, commands, GPU, VID, priority_level):
    boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
    cursor = boinc_db.cursor(buffered=True)

    insert_new_job = (
        "INSERT INTO volcon_jobs (token, Image, Command, Date_Sub, Notified, status, GPU, volcon_id, priority) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")

    cursor.execute(insert_new_job, (token, image, commands, timnow(), "0", "Received", GPU, VID, priority_level) )
    boinc_db.commit()



# Updates a certain VolCon ID with a new status
# Assumed to be non-locking
def update_job_status(VID, new_status, lock = False):

    if not lock:
        boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
        cursor = boinc_db.cursor(buffered=True)
        cursor.execute( "UPDATE volcon_jobs SET status = %s WHERE volcon_id = %s", (new_status, VID))
        boinc_db.commit()
    else:
        # TODO TODO TODO
        pass



# Updates the mirror ip
def update_mirror_ip(VID, mirror_ip):
    boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
    cursor = boinc_db.cursor(buffered=True)
    cursor.execute( "UPDATE volcon_jobs SET mirror_ip = %s WHERE volcon_id = %s", (mirror_ip, VID))
    boinc_db.commit()



# Returns the mirror IP for a certain VolCon ID
def get_mirror_for_job(VID):

    boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
    cursor = boinc_db.cursor(buffered=True)

    find_IP = ("SELECT mirror_ip FROM volcon_jobs WHERE volcon_id = %s")

    cursor.execute(insert_new_job, (VID) )

    for ips in cursor:
        # Only returns the first one
        return ips



# Finds available jobs
# A job is defined as available if (ERROR == NULL) and (status == 'Mirror received files')
# Filters by GPU (1: GPU is required, 0: GPU is not required)
# Filters by priority level
# Returns a list of VolCon IDs

def available_jobs(GPU_required, priority_level):

    boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
    cursor = boinc_db.cursor(buffered=True)

    find_VIDS = ("SELECT volcon_id, mirror_ip FROM volcon_jobs WHERE (ERROR IS NULL AND status = 'Mirror received files') AND (GPU = %s AND priority = %s)")
    cursor.execute(find_VIDS, (GPU_required, priority_level) )

    V = []
    for vid in cursor:
        V.append([vid[0], vid[1]])

    return V

