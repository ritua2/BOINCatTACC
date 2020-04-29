#!/usr/bin/env python3

"""
BASICS

Creates organization wide tokens, to be used when new researchers want to register
"""


import hashlib
import mysql.connector as mysql_con
import os
import random




Org_Name = str(input("Organization name: "))

given_password = str(input("Enter org password to add users: "))
orgtok = hashlib.sha256(given_password.encode('UTF-8')).hexdigest()

boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
cursor = boinc_db.cursor(buffered=True)

insert_new_job = (
    "INSERT INTO organizations (org_name, org_key) "
    "VALUES (%s, %s)")

cursor.execute(insert_new_job, (Org_Name, orgtok) )
boinc_db.commit()
cursor.close()
boinc_db.close()

print("New organization created: "+str(Org_Name))
