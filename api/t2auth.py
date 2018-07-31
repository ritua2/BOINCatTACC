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
import hashlib


r = redis.Redis(host='0.0.0.0', port=6389, db = 8)
r_org = redis.Redis(host = '0.0.0.0', port = 6389, db = 3)
app = Flask(__name__)


# Each user value in Redis will be stored as a hash (table) with multiple tokens assigned to it
# Each user is assigned to an organization, so there is no possible conflicts in case of multiple organizations present


# Gets the list of email addresses assigned to an user, or INVALID if he is not registered yet
# Requires the organization key due to security concerns
@app.route("/boincserver/v2/api/user_emails/<username>/<org_key>")
def user_emails(username, org_key):

    all_org_keys = [r_org.hmget(x.decode('UTF-8'), 'Organization Token')[0].decode('UTF-8') for x in r_org.keys()]
    if org_key not in all_org_keys:
       return 'Organization key invalid, access denied'

    # Gets the organization name
    for y in r_org.keys():
        syg = y.decode("UTF-8")
        if org_key == r_org.hmget(syg, 'Organization Token')[0].decode('UTF-8'):
            ORG = syg
            break

    # Checks if an organization has already been registered
    if ORG.encode() not in r.keys():
        return "NOT REGISTERED"

    # Checks if a user exists in an organization
    if username not in [r.lindex(ORG, w).decode('UTF-8') for w in range(0, r.llen(ORG))]:
        return "NOT REGISTERED"

    # The user is registered, so it returns a list of all its email addresses used so far (comma-separated)
    return ','.join([z.decode("UTF-8") for z in r.hkeys(username)])


# Gets the list of tokens for a given username
@app.route("/boincserver/v2/api/user_tokens/<username>/<org_key>")
def user_tokens(username, org_key):

    all_org_keys = [r_org.hmget(x.decode('UTF-8'), 'Organization Token')[0].decode('UTF-8') for x in r_org.keys()]
    if org_key not in all_org_keys:
       return 'Organization key invalid, access denied'

    # Gets the organization name
    for y in r_org.keys():
        syg = y.decode("UTF-8")
        if org_key == r_org.hmget(syg, 'Organization Token')[0].decode('UTF-8'):
            ORG = syg
            break

    # Checks if an organization has already been registered
    if ORG.encode() not in r.keys():
        return "NOT REGISTERED"

    # Checks if a user exists in an organization
    if username not in [r.lindex(ORG, w).decode('UTF-8') for w in range(0, r.llen(ORG))]:
        return "NOT REGISTERED"

    # The user is registered, so it returns a list of all its email addresses used so far (comma-separated)
    return ','.join([r.hget(username, z.decode("UTF-8")).decode("UTF-8") for z in r.hkeys(username)])


# Adds a username to the registered database, creates a new hash and updates the list if needed
# Hashes are needed since it is possible for a single user to have multiple emails assigned to their account
# If the user is already registered, it does nothing
@app.route("/boincserver/v2/api/add_username/<username>/<email>/<toktok>/<org_key>")
def add_username(username, email, toktok, org_key):

    org_key = hashlib.sha256(org_key.encode('UTF-8')).hexdigest()[:24:]

    all_org_keys = [r_org.hmget(x.decode('UTF-8'), 'Organization Token')[0].decode('UTF-8') for x in r_org.keys()]
    if org_key not in all_org_keys:
       return 'Organization key invalid, access denied'

    if pp.token_test(toktok) == False:
        return "INVALID token"

    for y in r_org.keys():
        if org_key == r_org.hmget(y, 'Organization Token')[0].decode('UTF-8'):
            ORG = y.decode('UTF-8')
            break


    # If the user is already registered it does nothing
    for qq in range(0, r.llen(ORG)):
        if username == r.lindex(ORG, qq).decode("UTF-8"):
            break
    else:
        # Adds a new row for the user
        r.rpush(ORG, username)
        # Creates a new hash
        r.hmset(username, {email:toktok})
        return "Added new username to the database"

    # Checks if the user has already set this email
    for zz in r.hkeys(username):
        if zz.decode('UTF-8') == email:
            return "User email already in database"

    # Adds another email to the user
    r.hset(username, email, toktok)

    return "Added another user email"



if __name__ == '__main__':
   app.run(host = '0.0.0.0', port = 5078)
