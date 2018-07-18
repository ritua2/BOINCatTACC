#!/usr/bin/env python3

"""
BASICS

Multiple operations to:
    - Assign usernames to tokens
    - Check if a username has any tokens assigned
    - Get all tokens assigned to an username
    - 
"""

import redis
from flask import Flask, request
import preprocessing as pp


r = redis.Redis(host='0.0.0.0', port=6389, db = 16)
r_org = redis.Redis(host = '0.0.0.0', port = 6389, db=3)
app = Flask(__name__)


# Each user value in Redis will be stored as a hash (table) with multiple tokens assigned to it
# Each user is assigned to an organization, so there is no possible conflicts in case of multiple organizations present


# Gets the list of email addresses assigned to an user, or INVALID if he is not registered yet
# Requires the organization key due to security concerns
@app.route("/boincserver/v2/api/user_emails/<username>/<org_key>")
def user_emails(username, org_key):

    all_org_keys = [r_org.hmget(x.decode('UTF-8'), 'Organization Token')[0].decode('UTF-8') for x in r_org.keys()]
    if orgtok not in all_org_keys:
       return 'Organization key invalid, access denied'

    # Gets the organization name
    for y in r_org.keys():
        if org_key == r_org.hmget(y, 'Organization Token')[0].decode('UTF-8'):
            ORG = y
            break

    # Checks if an organization has already been registered
    if ORG not in r.keys():
        return "NOT REGISTERED"

    # Checks if a user exists in an organization
    if username not in [r.lindex(ORG, w).decode('UTF-8') for w in range(0, r.llen(ORG))]:
        return "NOT REGISTERED"

    # The user is registered, so it returns a list of all its email addresses used so far (comma-separated)
    return ','.join([z.decode("UTF-8") for z in r.hkeys(username)])





if __name__ == '__main__':
   app.run(host = '0.0.0.0', port = 5078)
