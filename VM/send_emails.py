#!/usr/bin/env python3

"""
Send emails to users using linux command line called 'mail'
"""

from flask import Flask, request, jsonify, abort
import os
import socket

app = Flask(__name__)

@app.route("/send_emails", methods=['GET', 'POST'])
def send_emails():
    #All necessary information
    visitorIP = ""
    email_content = ""
    email_subject = ""
    user_email = ""

    #Get the visitor's IP
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
	visitorIP = request.environ['REMOTE_ADDR']
    else:
        visitorIP = request.environ['HTTP_X_FORWARDED_FOR']
    
    #Check the visistor's IP
    if (visitorIP == socket.gethostbyname(socket.gethostname())):
        try:
            email_content = request.form['email_content']
        except:
            raise SyntaxError("Missing parameter of the json: email_content")

        try:
            email_subject = request.form['email_subject']
        except:
            raise SyntaxError("Missing parameter of the json: email_subject")
        
        try:
            user_email = request.form['user_email']
        except:
            raise SyntaxError("Missing parameter of the json: user_email")

        send_email_command_line = 'echo "'+email_content+'" | mail -a FROM:t2b@tacc.utexas.edu -r no-reply@tacc.utexas.edu -s "'+email_subject+'" '+ user_email 
        try:
            os.system(send_email_command_line)
            return "Email Sent"
        except Exception as e:
            return e
    else:
        abort(404)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 6500, debug=True)
