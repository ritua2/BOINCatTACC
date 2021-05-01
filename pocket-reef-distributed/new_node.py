#!/usr/bin/env python3

"""
BASICS

Creates a new user, specified by their token
If the user already exists, an error result is returned
"""

import os, traceback
from flask import Flask, request
import base_functions as bf
import mysql.connector as mysql_con

app = Flask(__name__)
REEF_FOLDER = os.environ['Reef_Path']+"/sandbox/"


#################################
# CLUSTER ACTIONS
#################################

# returns ip_address of the instance
@app.route("/reef/cluster/whoami", methods=['GET'])
def whoami():
    IP_addr = request.environ['REMOTE_ADDR']
    return IP_addr

# Adds a new greyfish storage node to the cluster
@app.route("/reef/cluster/addme", methods=['POST'])
def cluster_addme():
    if not request.is_json:
        return "POST parameters could not be parsed"

    ppr = request.get_json()
    [error_occurs, missing_fields] = bf.error__l2_contains_l1(["MAX_STORAGE", "NODE_KEY"], ppr.keys())

    if error_occurs:
        return "INVALID: Lacking the following json fields to be read: "+missing_fields

    MAX_STORAGE = int(ppr["MAX_STORAGE"]) # in KB
    NODE_KEY = ppr["NODE_KEY"]
    IP_addr = request.environ['REMOTE_ADDR']

    grey_db = mysql_con.connect(host = os.environ["URL_BASE"] , port = 6602, user = os.environ["MYSQL_USER"] , password = os.environ["MYSQL_PASSWORD"], database = os.environ["MYSQL_DATABASE"])
    cursor = grey_db.cursor(buffered=True)
    cursor.execute("select * from node where ip=%s",(IP_addr,))
    uc=None
    for row in cursor:
        uc=row[0]
    cursor.close()
    grey_db.close()

    if uc != None:
        return "Node already attached"

    try:
        grey_db = mysql_con.connect(host = os.environ["URL_BASE"] , port = 6602, user = os.environ["MYSQL_USER"] , password = os.environ["MYSQL_PASSWORD"], database = os.environ["MYSQL_DATABASE"])
        cursor = grey_db.cursor(buffered=True)
        cursor.execute("insert into node(ip,total_space,free_space,node_key,status) values(%s,%s,%s,%s,'Available')",(IP_addr,MAX_STORAGE,MAX_STORAGE,NODE_KEY))
        grey_db.commit()
        cursor.execute("select name from user")
        users=[]
        for row in cursor:
            users.append(row[0])
        for user in users:
            cursor.execute("insert into file set ip=%s, user_id=%s, id='', directory='', is_dir=TRUE",(IP_addr,user))
            cursor.execute("insert into file set ip=%s, user_id=%s, id='', directory='___RESULTS', is_dir=TRUE",(IP_addr,user))
        grey_db.commit()
        cursor.close()
        grey_db.close()
        return "New node attached correctly"
    except:
        traceback.print_exc()
        return "INVALID, Server Error: Could not connect to database"

if __name__ == '__main__':
   app.run()
