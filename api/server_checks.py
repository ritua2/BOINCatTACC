#!/usr/bin/env python3

"""
BASICS

Checks the server status and validity of tokens.
Does not include any submission APIs.
"""


from flask import Flask, jsonify
import mysql.connector as mysql_con
import os



app = Flask(__name__)

# Basic operational check
@app.route("/boincserver/v2/api_status")
def api_operational():
    return 'Server APIs are active'


# Tutorial
@app.route("/boincserver/v2/api_tutorial")
def tutorial():
   
   full = {'Ports' : {'5000': 'Tutorial and health-checks',
                      '5075': 'Known image job submission, text file',
                      '5085': 'Unknown image job submission, follow instructions'
                      },
    'Disclaimer': 'API usage is restricted to users with granted access, Token required. To test token, curl -> http://{BOINC_IP}:5000/boincserver/test_token=ENTER_TOKEN',
    'User guide': {'Known images': {'Single job': 'Not allowed, use a single-line text file instead',
                                   'Multiple job': {'Instructions':'Follow the text file at SERVER/boincserver/submit_multi',
                                                     'Curl Example': 'curl  -F file=@Example_multi_submit.txt http://129.114.16.27:5075/boincserver/v2/submit_known/token=pRPDriRP62JVKw'
                                                    }
                                   }
                  }
    }

   return jsonify(full)


# Token test
@app.route("/boincserver/v2/token_test=<token>")
def token_test(token):

    boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
    cursor = boinc_db.cursor(buffered=True)
    cursor.execute("SELECT token FROM researcher_users WHERE token = %s", (token,) )

    for user_email in cursor:
        # Exists
        cursor.close()
        boinc_db.close()
        return "Accepted"

    cursor.close()
    boinc_db.close()
    # Does not exist
    return "Invalid"



if __name__ == '__main__':
   app.run(host ='0.0.0.0', port = 5000, debug=False, threaded=True)
