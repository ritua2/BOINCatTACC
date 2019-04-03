#!/usr/bin/env python3

"""
Send emails to users using linux command line called 'mail'
"""

from flask import Flask, request, jsonify, abort
import os
import socket
from IPy import IP

app = Flask(__name__)

@app.route("/send_emails", methods=['GET', 'POST'])
def send_emails():
    #All necessary information
    visitorIP = ""
    email_content = ""
    email_subject = ""
    user_email = ""
    sender_email = "t2b@tacc.utexas.edu"

    #Get the visitor's IP
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
	visitorIP = request.environ['REMOTE_ADDR']
    else:
        visitorIP = request.environ['HTTP_X_FORWARDED_FOR']

    #print("visitorIP: " + IP(visitorIP).iptype().lower())
    #print("hostname: " + socket.gethostbyname(socket.gethostname()))
    
    #Check the visistor's IP
    if (visitorIP == socket.gethostbyname(socket.gethostname()) or IP(visitorIP).iptype().lower() == "private"):
        try:
            jsonDict = request.get_json()
        except:
            return "Cannot parse the json"

        try:
            email_content = jsonDict['email_content']
        except:
            return "Missing parameter of the json: email_content"

        try:
            email_subject = jsonDict['email_subject']
        except:
            return "Missing parameter of the json: email_subject"
        
        try:
            user_email = jsonDict['user_email']
        except:
            return "Missing parameter of the json: user_email"

	#print("content: "+email_content+"subject: "+email_subject+"user_email: "+user_email)
        send_email_to_user = 'echo "'+email_content+'" | mail -s "'+email_subject+'" '+ user_email 
        send_email_to_t2b = 'echo "'+email_content+'" | mail  -s "'+email_subject+'" '+ sender_email 

        try:
            os.system(send_email_to_user)
            os.system(send_email_to_t2b)
            return "Email Sent"
        except Exception as e:
            return e
    else:
        abort(404)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5020, debug=True)
