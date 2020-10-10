#create directories for all researchers

import mysql.connector as mysql_con
import os
import requests

boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
cursor = boinc_db.cursor()
cursor.execute("SELECT token FROM researcher_users")

for user_tok in cursor:
    if not os.path.exists("/home/boincadm/project/api/sandbox_files/DIR_"+user_tok[0]):
        # Also creates a Reef directory
        requests.get('http://'+os.environ['Reef_IP']+':2002/reef/create_user/'+user_tok[0]+'/'+os.environ['Reef_Key'])

        # Creates also the local directories for MIDAS usage
        os.mkdir("/home/boincadm/project/api/sandbox_files/DIR_"+user_tok[0])
        os.mkdir("/home/boincadm/project/api/sandbox_files/DIR_"+user_tok[0]+'/___RESULTS')

cursor.close()
boinc_db.close()