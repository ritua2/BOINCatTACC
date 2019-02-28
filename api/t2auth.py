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


r_org = redis.Redis(host = '0.0.0.0', port = 6389, db = 3)
r = redis.Redis(host='0.0.0.0', port=6389, db = 8)
app = Flask(__name__)



# Finds an organization for a given key
# Returns False if not
def get_user_org(ORG_KEY):

    HOK = hashlib.sha256(ORG_KEY.encode('UTF-8')).hexdigest()

    # Finds if an organization is allowed
    for one_org in r_org.hkeys("ORGS"):
        # Accounts for keys already provided as a hash
        if (HOK == r_org.hget("ORGS", one_org.decode("UTF-8")).decode("UTF-8")) or (ORG_KEY == r_org.hget("ORGS", one_org.decode("UTF-8")).decode("UTF-8")):
            return one_org.decode("UTF-8")
    else:
        return False



# Each user value in Redis will be stored as a hash (table) with multiple tokens assigned to it
# Each user is assigned to an organization, so there is no possible conflicts in case of multiple organizations present


# Gets the list of email addresses assigned to an user, or INVALID if he is not registered yet
# Requires the organization key due to security concerns
@app.route("/boincserver/v2/api/user_emails/<username>/<org_key>")
def user_emails(username, org_key):


    ORG = get_user_org(org_key)

    if ORG == False:
        return 'Organization key invalid, access denied'

    # Checks if a user exists in an organization
    if username not in [r.lindex(ORG, w).decode('UTF-8') for w in range(0, r.llen(ORG))]:
        return "NOT REGISTERED"

    # The user is registered, so it returns a list of all its email addresses used so far (comma-separated)
    return ','.join([z.decode("UTF-8") for z in r.hkeys(username)])


# Gets the list of tokens for a given username
@app.route("/boincserver/v2/api/user_tokens/<username>/<org_key>")
def user_tokens(username, org_key):

    ORG = get_user_org(org_key)

    if ORG == False:
        return 'Organization key invalid, access denied'

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

    ORG = get_user_org(org_key)

    if ORG == False:
        return 'Organization key invalid, access denied'

    if pp.token_test(toktok) == False:
        return "INVALID token"

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
   app.run(host = '0.0.0.0', port = 5078, debug=False, threaded=True)
