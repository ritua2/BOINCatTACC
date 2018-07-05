#!/usr/bin/env python3

"""
BASICS

Communicates with adtdp clients.
sends tar archives with instructions and receives the results
"""

import redis
import random
import json
import os, shutil
from flask import Flask, request, send_file
import preprocessing as pp


r = redis.Redis(host = '0.0.0.0', port = 6389, db = 14)
app = Flask(__name__)

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

    #r.hset(work_ID, "Error", "Running")

    return send_file("/root/project/adtd-protocol/tasks/"+work_ID+"/tbp.tar.gz")




if __name__ == '__main__':
   app.run(host = '0.0.0.0', port = 5095)
