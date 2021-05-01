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


# toktok (str): User token
# Creates a user
@app.route("/reef/create_user/<toktok>/<rkey>")
def create_user(toktok,rkey):

    if not bf.valid_key(rkey):
        return "INVALID key, cannot create a new user"

    # Stores usernames in MYSQL since this will be faster to check in the future
    grey_db = mysql_con.connect(host = os.environ["URL_BASE"] , port = 6602, user = os.environ["MYSQL_USER"] , password = os.environ["MYSQL_PASSWORD"], database = os.environ["MYSQL_DATABASE"])
    cursor = grey_db.cursor(buffered=True)
    cursor.execute("select * from user where name=%s",(toktok,))
    uc=None
    for row in cursor:
        uc=row[0]
    cursor.close()
    grey_db.close()

    if uc != None:
        return "User already has an account"

    print('User doesn\'t exist')

    try:
        grey_db = mysql_con.connect(host = os.environ["URL_BASE"] , port = 6602, user = os.environ["MYSQL_USER"] , password = os.environ["MYSQL_PASSWORD"], database = os.environ["MYSQL_DATABASE"])
        cursor = grey_db.cursor(buffered=True)
        cursor.execute("insert into user(name) values(%s)",(toktok,))
        grey_db.commit()
        cursor.execute("select ip from node")
        nodes=[]
        for row in cursor:
            nodes.append(row[0])
        for node in nodes:
            cursor.execute("insert into file set ip=%s, user_id=%s, id='', directory='', is_dir=TRUE",(node,toktok))
            cursor.execute("insert into file set ip=%s, user_id=%s, id='', directory='___RESULTS', is_dir=TRUE",(node,toktok))
        grey_db.commit()
        cursor.close()
        grey_db.close()
        return "Reef cloud storage now available"
    except:
        traceback.print_exc()
        return "INVALID, Server Error: Could not connect to database"

if __name__ == '__main__':
   app.run(host = '0.0.0.0', port = 2002)
