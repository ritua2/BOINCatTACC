"""
BASICS

Sends a researcher an email when a job has been completed
"""

import mysql.connector as mysql_con


boinc_db = mysql_con.connect(host = '129.114.16.27', port = 3306, user = 'root', password = '', database = 'boincserver')

cursor = boinc_db.cursor()

# Choose only those units that have been completed
query = ("SELECT name, server_state, outcome FROM result")

cursor.execute(query)

for (name, server_state, outcome) in cursor:
     print(name, server_state, outcome)

cursor.close()
boinc_db.close()
