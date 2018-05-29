"""
BASICS

Checks the server status and validity of tokens.
Does not include any submission APIs.
"""

from flask import Flask, jsonify

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
    'Disclaimer': 'API usage is restricted to users with granted access, Token required. To test token, curl ->\
                  http://{BOINC_IP}:5000/boincserver/test_token=ENTER_TOKEN',
    'User guide': {'Known images': {'Single job': 'Not allowed, use a single-line text file instead'},
                                   {'Multiple job': {'Instructions':'Follow the text file at SERVER/boincserver/submit_multi',
                                                     'Curl Example': 'curl  -F file=@Example_multi_submit.txt http://129.114.16.27:5075/boincserver/v2/submit_known/token=pRPDriRP62JVKw'
                                                    }
                                   }
                  }
    }

   return jsonify(full)


# Token test
@app.route("/boincserver/v2/token_test=<token>")
def token_test(token):

   if len(token) < 14:
   	   return 'Invalid'

   with open("../html/user/token_data/Tokens.txt", "r") as TFIL:
       for line in TFIL:
           if token in line:
              return 'Accepted'
       else:
           return 'Invalid'


if __name__ == '__main__':
   app.run(host ='0.0.0.0', port = 5000)
