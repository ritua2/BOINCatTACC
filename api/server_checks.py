"""
BASICS

Checks the server status and validity of tokens.
Does not include any submission APIs.
"""

from flask import Flask

app = Flask(__name__)

@app.route("/boincserver/api_status")
def api_operational():
    return 'Server APIs are active'

if __name__ == '__main__':
   app.run(host ='0.0.0.0', port = 5000)