#!/usr/bin/env python3

"""
BASICS

Get all tokens assigned to an username
"""


from flask import Flask, request


import mysql_interactions as mints



app = Flask(__name__)


# Gets the list of tokens for a given username
# Can only be called from within the server itself
@app.route("/boincserver/v2/api/user_tokens/<username>")
def user_tokens(username):

        #Get the visitor's IP
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        visitorIP = request.environ['REMOTE_ADDR']
    else:
        visitorIP = request.environ['HTTP_X_FORWARDED_FOR']
   
    #Check the visistor's IP
    if visitorIP != "127.0.0.1":
        return "INVALID IP"

    token_list = mints.user_tokens(username)

    if len(token_list) == 0:
        return "NOT REGISTERED"

    # The user is registered, so it returns a list of all its email addresses used so far (comma-separated)
    return ','.join(token_list)



if __name__ == '__main__':
   app.run(host = '0.0.0.0', port = 5078, debug=False, threaded=True)
