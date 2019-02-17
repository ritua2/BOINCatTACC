#!/usr/bin/env python3

"""
BASICS

Checks if a user is accredited by LDAP or not
Since the app runs on , it cannot be accessed from outside the server
"""


from flask import Flask
from ldap3 import Server, Connection, ALL



app = Flask(__name__)


# Checks if the user is validated through ldap
@app.route("/boincserver/v2/api/ldap_check/<username>/<pw>")
def ldap_check(username, pw):

    s = Server('ldap.tacc.utexas.edu', port=389, get_info=ALL)
    c = Connection(s, user='uid='+username+",ou=People,dc=tacc,dc=utexas,dc=edu", password=pw)

    if not c.bind():
        return "INVALID, user is not registered or invalid credentials"

    return "User is authenticated"




if __name__ == '__main__':
   app.run(host = '0.0.0.0', port = 6032, debug=False, threaded=True)
