#!/usr/bin/env python3

"""
BASICS


Returns a researcher's data in a JSON form
"""

import datetime
from flask import Flask, jsonify
import mysql.connector as mysql_con
import os
import preprocessing as pp
import redis



app = Flask(__name__)
r_data = redis.Redis(host='0.0.0.0', port=6389, db=0)
r_alloc = redis.Redis(host='0.0.0.0', port=6389, db=2)



# Returns a list of Image, Command, Date (Sub), Date (Run), Received time
def VolCon_info(token):
    boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
    cursor = boinc_db.cursor(buffered=True)
    cursor.execute("SELECT Image, Command, Date_Sub, Date_Run, received_time, status FROM volcon_jobs WHERE Token = %s", (token,) )

    HJK = []

    for ips in cursor:
        Image = ips[0]
        CC = ips[1]
        datesub = ips[2].replace(microsecond=0).isoformat()
        daterun = ips[3]
        if daterun == None:
            daterun = ips[5]
        else:
            daterun = daterun.replace(microsecond=0).isoformat()
        email_notified = ips[4]
        if email_notified == None:
            email_notified = ""
        else:
            email_notified = email_notified.replace(microsecond=0).isoformat()

        HJK.append([{"Image":Image, "Command":CC, "Date (Sub)":datesub, "Date (Run)":daterun, "Notified":email_notified}]) 

    cursor.close()
    boinc_db.close()
    # Does not exist
    return HJK



def transform_to_iso(maybe_date):

    try:
        return datetime.datetime.strptime(maybe_date, "%Y-%m-%d %H:%M:%S").replace(microsecond=0).isoformat()
    except:
        # It is an error message, or empty
        return maybe_date



@app.route("/boincserver/v2/api/user_data/personal/<toktok>")
def user_data(toktok):

    if pp.token_test(toktok) == False:
       return 'INVALID token'

    U_alloc = r_alloc.get(toktok).decode("UTF-8")

    # Finds all the data
    totjobs = r_data.llen("Token")

    U_data = []
    for qq in range(0, totjobs):
        if r_data.lindex("Token", qq).decode("UTF-8") == toktok:
            # [[Image, Command, Date (Sub), Date (Run), Notified], ..]
            U_data.append([])
            curdat = {}
            imnam = r_data.lindex("Image", qq).decode("UTF-8")
            if "carlosred/" != imnam[:10:]:
                imnam += " (CUSTOM)"
            curdat["Image"] = imnam
            curdat["Command"] = r_data.lindex("Command", qq).decode("UTF-8")
            curdat["Date (Sub)"] = transform_to_iso(r_data.lindex("Date (Sub)", qq).decode("UTF-8"))
            curdat["Date (Run)"] = transform_to_iso(r_data.lindex("Date (Run)", qq).decode("UTF-8"))
            curdat["Notified"] = transform_to_iso(r_data.lindex("Notified", qq).decode("UTF-8"))
            U_data[-1].append(curdat)

    # Appends the VolCon jobs
    vc_info = VolCon_info(toktok)
    U_data = U_data + vc_info

    # Sorts them by received date
    U_data = sorted(U_data, key = lambda x: x[0]["Date (Sub)"])

    return jsonify({"allocation":U_alloc, "job data":U_data})



# Obtains all the userdata associated with a certain username
@app.route("/boincserver/v2/api/user_data/personal/by_username/<username>")
def user_data_by_username(username):

    # Obtains a database connection
    boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
    cursor = boinc_db.cursor(buffered=True)
    cursor.execute("""
        SELECT Image, Command, date_processed, date_run, date_notified, status FROM boinc2docker_jobs WHERE username = %s
        UNION
        SELECT Image, Command, Date_Sub AS date_processed, Date_Run, received_time, status FROM volcon_jobs WHERE username = %s
        ORDER BY date_processed DESC LIMIT 100""", (username, username) )

    jobs_submitted_data = []

    for ips in cursor:
        Image = ips[0]
        CC = ips[1]
        datesub = ips[2].strftime("%Y-%m-%d %H:%M:%S")
        daterun = ips[3]
        if daterun == None:
            daterun = ips[5]
        else:
            daterun = daterun.strftime("%Y-%m-%d %H:%M:%S")
        email_notified = ips[4]
        if email_notified == None:
            email_notified = ""
        else:
            email_notified = email_notified.strftime("%Y-%m-%d %H:%M:%S")

        jobs_submitted_data.append([{"Image":Image, "Command":CC, "Date (Sub)":datesub, "Date (Run)":daterun, "Notified":email_notified}])

    # Closes database connection
    cursor.close()
    boinc_db.close()

    return jsonify({"job data":jobs_submitted_data})


if __name__ == '__main__':
   app.run(host = '0.0.0.0', port = 5092, debug=False, threaded=True)
