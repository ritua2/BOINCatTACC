#!/usr/bin/env python3

"""
BASICS

Communicates with adtdp clients.
sends tar archives with instructions and receives the results
"""

import redis
import random
import json
import datetime
import os, shutil
from flask import Flask, request, send_file, jsonify
from werkzeug.utils import secure_filename
import preprocessing as pp


r = redis.Redis(host = '0.0.0.0', port = 6389, db = 14)
r_run = redis.Redis(host = '0.0.0.0', port = 6389, db =0)
UPLOAD_FOLDER = "/results/adtdp/"
TASKS_FOLDER = "/home/boincadm/project/adtd-protocol/tasks/"
app = Flask(__name__)


# Ensures that the server is ADTDP available
@app.route("/boincserver/v2/api/adtdp_server")
def adtdp_server():
    return "Server is ADTDP able"


# Returns if there are available jobs
@app.route("/boincserver/v2/api/available_adtdp")
def available_adtdp():

	all_jobs = [x.decode('UTF-8') for x in r.keys()]
	ava_jobs = [y for y in all_jobs if r.hget(y, "Error").decode("UTF-8") == "Not Run"]

	if len(ava_jobs) == 0:
		return "No jobs available"

	return ", ".join(ava_jobs)


# Given a specific job ID, it returns said job
# Updates the database to enforce that no other process can run this job again
@app.route("/boincserver/v2/api/adtdp/request_work", methods = ['GET', 'POST'])
def request_work():

    if request.method != "POST":
        return "INVALID, no data provided"

    try:
        work_ID = request.form["work_ID"]
    except:
        return "INVALID, no data provided"

    if work_ID == '':
        return "INVALID, no data provided"

    all_jobs = [x.decode('UTF-8') for x in r.keys()]
    ava_jobs = [y for y in all_jobs if r.hget(y, "Error").decode("UTF-8") == "Not Run"]

    if work_ID not in ava_jobs:
        return "INVALID, job ID is not available"

    r.hset(work_ID, "Error", "Running")
    return send_file("/home/boincadm/project/adtd-protocol/tasks/"+work_ID+"/tbp.tar.gz")


# Erases a job when it returns an error
@app.route("/boincserver/v2/api/adtdp/failed_job", methods = ["GET", "POST"])
def failed_job():

    if request.method != "POST":
        return "INVALID, no data provided"

    try:
        work_ID = request.form["work_ID"]
    except:
        return "INVALID, no data provided"

    if work_ID == '':
        return "INVALID, no data provided"

    all_jobs = [x.decode('UTF-8') for x in r.keys()]
    ava_jobs = [z for z in all_jobs if r.hget(z, "Error").decode("UTF-8") == "Running"]

    if work_ID not in ava_jobs:
        return "INVALID, job ID is not available"

    # Changes the status
    r.hset(work_ID, "Error", "Failed")
    r.delete(work_ID)
    # Updates the main database
    for nvnv in range(0, r_run.llen('Token')):

        if work_ID in r_run.lindex("Error", nvnv).decode("UTF-8"):
            r_run.lset("Date (Run)", nvnv, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            r_run.lset("Error", nvnv, work_ID+"| Failed")
            break

    return "Succesfully updated failed job DB"


# Updates the database for succesful jobs
@app.route("/boincserver/v2/api/adtdp/succesful_job", methods=["GET", "POST"])
def succesful_job():

    if request.method != "POST":
        return "INVALID, no data provided"

    try:
        work_ID = request.form["work_ID"]
        good_results = request.form["gr"]
        bad_results = request.form["br"]
    except:
        return "INVALID, no data provided"

    if work_ID == '':
        return "INVALID, no data provided"

    try:
        file = request.files["resfil"]
    except:
        return "INVALID, file not provided"

    all_jobs = [x.decode('UTF-8') for x in r.keys()]
    ava_jobs = [z for z in all_jobs if r.hget(z, "Error").decode("UTF-8") == "Running"]

    if work_ID not in ava_jobs:
        return "INVALID, job ID is not available"

    for nvnv in range(0, r_run.llen('Token')):

        if work_ID in r_run.lindex("Error", nvnv).decode("UTF-8"):
            prestime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            r_run.lset("Date (Run)", nvnv, prestime)
            r_run.lset("Error", nvnv, work_ID+" | Success | "+good_results+","+bad_results)
            break

    # Moves the file
    new_name = secure_filename(file.filename)
    # Creates a new directory if it does not exist
    short_date = prestime.split(" ")[0]
    if short_date not in os.listdir(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER+short_date)

    file.save(os.path.join(UPLOAD_FOLDER+short_date, new_name))
    # Changes the name
    shutil.move(UPLOAD_FOLDER+short_date+"/"+new_name, UPLOAD_FOLDER+short_date+"/"+work_ID+".tar.gz")
    # Deletes the information file
    shutil.rmtree(TASKS_FOLDER+work_ID)

    r.hset(work_ID, "Error", "Success")
    return "Succesfully updated succesful job DB"


# Returns job information for a work ID in adtd-p only
@app.route("/boincserver/v2/api/adtdp/info/<work_ID>")
def info(work_ID):

    return jsonify({k.decode('utf8'): v.decode('utf8') for k, v in  r.hgetall(work_ID).items()})



if __name__ == '__main__':
   app.run(host = '0.0.0.0', port = 5095, debug=False, threaded=True)
