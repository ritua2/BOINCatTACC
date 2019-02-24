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
def add_job(token, image, commands, GPU):
    boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = 'root', password = '', database = 'boincserver')
    cursor = boinc_db.cursor(buffered=True)



    insert_new_job = (
        "INSERT INTO volcon_jobs (token, Image, Command, Date_Sub, Notified, status, GPU) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s)")

    cursor.execute(insert_new_job, (token, image, commands, timnow(), "0", "Received", GPU) )
    boinc_db.commit()
