"""
BASICS


MIDAS: Multiple Input Docker Automation System

Generates a github image with all user commands inside to be submitted to BOINC
"""

from flask import Flask, jsonify
import tarfile, shutil, os


app = Flask(__name__)

# Basic operational check
@app.route("/boincserver/v2/midas_status")
def api_operational():
    return 'MIDAS APIs are active'

# MIDAS tutorial
# Tutorial
@app.route("/boincserver/v2/midas_tutorial")
def tutorial():
   
    full = {
    'Basics' : 'MIDAS (Multiple Input Docker Automation System) is a TACC developed tool ',
    'Disclaimer': 'API usage is restricted to users with granted access, Token required. To test token, curl ->\
                  http://{BOINC_IP}:5000/boincserver/test_token=ENTER_TOKEN',
    'User guide': {'Steps': 'Submit a tar.gz file containing a compressed folder with all the files. File must be a tar.gz , all other inputs will not be accepted .',
                   'Contents' : 'All files must contain a README.txt (file ending MUST be .txt, all other inputs will not be accepted',
                   'README.txt': 'Follow instructions, curl -> http://SERVER_IP/boincserver/README_MIDAS_example.txt',

                   'Other files': 'Their number and name must be accounted for in the README',
                   'Outputs': 'Their full path must be included'            

                  },
                  
    'Limitations': 'MIDAS is based on Docker publicly available Docker images. As such, only open-source, free to use software is allowed. No Intel compilers, software that requires key access, enterprise editions, or private OS (Windows, Mac are not allowed)'
    'Supported Languages': {'Current': 'None',
                            'Short Term Future Updates':'Python, Go, Bash scripts (Short Term)',
                            'Long Term Future Updates':'Haskell, OCaml, C, C++'
                           },

    'Root Access': 'Assume root access when installing dependencies trough a bash script'

    }

    return jsonify(full)



if __name__ == '__main__':
   app.run(host ='0.0.0.0', port = 5085)
