#!/usr/bin/env python3

"""
BASICS

Provides the framework to assign tokens based on a 2 factor authorization
"""

import redis
import random
import json
from flask import Flask, request
from werkzeug.datastructures import ImmutableMultiDict
import preprocessing as pp


r_alloc = redis.Redis(host = '0.0.0.0', port = 6389, db =2)
r_org = redis.Redis(host = '0.0.0.0', port = 6389, db=3)
r_temp = redis.Redis(host = '0.0.0.0', port = 6389, db = 4)
app = Flask(__name__)


# Verifies if 2-factr token APIs are active
@app.route("/boincserver/v2/api/token-2factor")
def factor2_operational():
    return '2-Factor token generation is active'


# Verifies if an user's organization is allowed
@app.route("/boincserver/v2/api/verify_org/<orgtok>")
def verify_org(orgtok):
    all_org_keys = [r_org.hmget(x.decode('UTF-8'), 'Organization Token')[0].decode('UTF-8') for x in r_org.keys()]
    if orgtok in all_org_keys:
       return 'Organization key is valid'

    return 'Organization token is invalid, access denied'


# Allows to request a temporary token for an user to be used later
@app.route("/boincserver/v2/api/request_user_token/<orgtok>", methods = ['GET', 'POST'])
def request_user_token(orgtok):
    if request.method != 'POST':
       return 'Invalid, no data provided'

    all_org_keys = [r_org.hmget(x.decode('UTF-8'), 'Organization Token')[0].decode('UTF-8') for x in r_org.keys()]
    if orgtok not in all_org_keys:
       return 'Organization key invalid, access denied'

    dictdata = ImmutableMultiDict(request.form).to_dict(flat='')
    NAME = str(dictdata['name'][0])
    LAST_NAME = str(dictdata['last_name'][0])
    EMAIL = str(dictdata['email'][0])
    if '' in [NAME, LAST_NAME, EMAIL]:
       return 'Invalid request, not all information has been provided'
    # Creates a temporary token, sent to the user's email
    SEQ = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    temptok = ''
    for qq in range(0, 24):
        temptok += random.choice(SEQ)

    Text = "Your token request has been approved.\nYour token is:    "+temptok+"\n\n\nInsert this token in the second step when prompted\n\n"
    Text += "Note: This is an automated message, all messages sent to this address will be ignored."
    r_temp.setex(temptok, 'valid', 24*3600) # Redis documentation is faulty, time goes at the end
    pp.send_mail(EMAIL, 'Temporary token requested', Text)
    return 'An automatic email has been sent to the provided email address, this token will remain valid for 24 hours.'


# Checks the company's maximum allocation
@app.route("/boincserver/v2/api/check_company_allocation/<orgtok>")
def check_company_allocation(orgtok):

    all_org_keys = [r_org.hmget(x.decode('UTF-8'), 'Organization Token')[0].decode('UTF-8') for x in r_org.keys()]
    if orgtok not in all_org_keys:
       return 'Organization key invalid, access denied'

    all_orgs = [x.decode('UTF-8') for x in r_org.keys()]
    for otok, org in zip(all_org_keys, all_orgs):
        if otok == orgtok:
           user_org = org

    return r_org.hget(user_org, 'Data Plan').decode('UTF-8')


# Verifies the user's token and creates a new user for BOINC
# Establishes user's allocation
# Assigns the user to an organization
# Deletes the temporary tokens
@app.route("/boincserver/v2/api/authenticated_request_token/<orgtok>/<temptok>", methods = ['GET', 'POST'])
def authenticated_request_token(orgtok, temptok):

    if request.method != 'POST':
       return 'Invalid, no data provided'

    all_org_keys = [r_org.hmget(x.decode('UTF-8'), 'Organization Token')[0].decode('UTF-8') for x in r_org.keys()]
    if orgtok not in all_org_keys:
       return 'Organization key invalid, access denied'

    if r_temp.get(temptok) is None:
       return 'Temporary token not valid or expired, access denied'

    dictdata = ImmutableMultiDict(request.form).to_dict(flat='')
    try:
       NAME = str(dictdata['name'][0])
       LAST_NAME = str(dictdata['last_name'][0])
       EMAIL = str(dictdata['email'][0])
       ALLOCATION = str(dictdata['allocation'][0])

    except:
       return 'Invalid request, not all data is provided'

    # Finds the organization's name and updates it with the result
    all_orgs = [x.decode('UTF-8') for x in r_org.keys()]
    for otok, org in zip(all_org_keys, all_orgs):
        if otok == orgtok:
           user_org = org
    
    maxalloc = r_org.hget(user_org, 'Data Plan').decode('UTF-8')
    if float(ALLOCATION) > float(maxalloc):
       return 'Invalid: User requested allocation is larger than organization allows'

    # Creates a final token for the user
    SEQ = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    user_tok = ''
    for qq in range(0, 14):
        user_tok += random.choice(SEQ)
    
    # Replaces single quotes by double quotes
    Org_Users_Data = json.loads(r_org.hget(user_org, 'Users').decode('UTF-8').replace('\"', 'UHJKNM').replace('\'', '\"').replace('UHJKLM', '\''))
    Org_Users_Data[user_tok]={'name':NAME, 'last name':LAST_NAME, 'email':EMAIL, 'allocation':ALLOCATION}
    r_org.hset(user_org, 'Users', Org_Users_Data)
    r_temp.delete(temptok)
    r_org.hincrby(user_org, 'No. Users', 1)

    # Adds the token to the token file
    with open("/root/project/html/user/token_data/Tokens.txt", "a") as tokfile:
         tokfile.write(NAME+" "+LAST_NAME+", "+user_tok+", "+EMAIL+'\n')

    # Adds the allocation details
    r_alloc.set(user_tok, ALLOCATION)

    return 'User has been added, your new token is: '+user_tok



if __name__ == '__main__':
   app.run(host = '0.0.0.0', port = 5054)
