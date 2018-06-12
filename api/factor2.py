#!/usr/bin/env python3

"""
BASICS

Provides the framework to assign tokens based on a 2 factor authorization
"""

import redis
from flask import Flask, request
import preprocessing as pp


r_org = redis.Redis(host = '0.0.0.0', port = 6389, db=3)
r_temp = redis.Redis(host = '0.0.0.0', port = 6389, db = 4)
app = Flask(__name__)


# Verifies if 2-factr token APIs are active
@app.route("/boincserver/v2/api/token-2factor")
def factor2_operational():
    return '2-Factor token generation is active'






if __name__ == '__main__':
   app.run(host = '0.0.0.0', port = 5054)
