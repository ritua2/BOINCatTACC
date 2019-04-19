#!/usr/bin/env python3

"""
BASICS

Checks if a user is accredited by LDAP or not
Since the app runs on , it cannot be accessed from outside the server
"""


from flask import Flask
from ldap3 import Server, Connection, ALL
import logging
import os, sys



app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)



# Checks if the user is validated through ldap
@app.route("/boincserver/v2/api/ldap_check/<username>/<pw>")
def ldap_check(username, pw):

    if os.environ["dev_yn"] == "y":
        return True

    s = Server('ldap.tacc.utexas.edu', port=389, get_info=ALL)
    c = Connection(s, user='uid='+username+",ou=People,dc=tacc,dc=utexas,dc=edu", password=pw)

    if not c.bind():
        return "INVALID, user is not registered or invalid credentials"
    return "User is authenticated"




if __name__ == '__main__':
   app.run(host = '0.0.0.0', port = 6032, debug=False, threaded=True)
