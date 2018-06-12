#!/usr/bin/env python3

"""
BASICS

Provides the framework to assign tokens based on a 2 factor authorization
"""

import redis
from flask import Flask, request
from werkzeug.datastructures import ImmutableMultiDict
import preprocessing as pp


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
    NAME = str(dictdata['name'])
    LAST_NAME = str(dictdata['last_name'])
    EMAIL = str(dictdata['email'])
    if '' in [NAME, LAST_NAME, EMAIL]:
       return 'Invalid request, not all information has been provided'
    # Creates a temporary token, sent to the user's email
    SEQ = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    temptok = ''
    for qq in range(0, 24):
        temptok += random.choice(SEQ)

    Text = "Your token request has been approved.\nYour token is:    "+temptok+"\n\n\nInsert this token in the second step when prompted\n\n"
    Text += "Note: This is an automated message, all messages sent to this address will be ignored."


if __name__ == '__main__':
   app.run(host = '0.0.0.0', port = 5054)
