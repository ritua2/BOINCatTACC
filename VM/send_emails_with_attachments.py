#!/usr/bin/env python3

"""
Send emails to users using linux command line called 'mail'
Admits attachments as long as the file exists
"""

from flask import Flask, request, jsonify, abort
import os
import socket
from werkzeug.utils import secure_filename
from IPy import IP

app = Flask(__name__)
email_results_directory = "/email_data/"




# Stores a file in a temporary location within the server: /email_data
@app.route("/emails/provide_file", methods=['POST'])
def provide_file():

    file = request.files['file']

    # Avoids empty filenames and those with commas
    if file.filename == '':
       return 'INVALID, no file uploaded'
    new_name = secure_filename(file.filename)

    file.save(email_results_directory+new_name)
    return "File saved in the main server"



# Adds the needed full path information to the file
def full_path_for_email(just_filename):
    return email_results_directory+just_filename



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

        # Checks if there are attachments
        if "attachments" in jsonDict:
            attachments = jsonDict["attachments"]
        else:
            attachments = []

	   #print("content: "+email_content+"subject: "+email_subject+"user_email: "+user_email)
        send_email_to_user = 'echo "'+email_content+'" | mail -s "'+email_subject+'" ' 
        send_email_to_t2b = 'echo "'+email_content+'" | mail  -s "'+email_subject+'" '


        corrected_filenames = []

        # Sends the file and deletes the local copy since there is no use for it in the local server
        for file_name in attachments:
            correct_file_path = full_path_for_email(file_name)

            if not os.path.isfile(correct_file_path):
                # Fail silently
                continue

            send_email_to_user += " -A "+correct_file_path
            send_email_to_t2b  += " -A "+correct_file_path
            corrected_filenames.append(correct_file_path)

        # Adds the emails at the end
        send_email_to_user += " "+ user_email 
        send_email_to_t2b += " "+ sender_email

        try:
            os.system(send_email_to_user)
            os.system(send_email_to_t2b)

            for fnam in corrected_filenames:
                os.remove(fnam)

            return "Email Sent"
        except Exception as e:
            return e
    else:
        abort(404)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5021, debug=True)
