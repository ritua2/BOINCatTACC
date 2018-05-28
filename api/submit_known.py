"""
BASICS

Automated job submission for known Docker images through APIs
"""

import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import preprocessing as pp
import glob
import redis
import datetime


r = redis.Redis(host= '0.0.0.0', port = 6389, db =0)
app = Flask(__name__)


if __name__ == '__main__':
   app.run(host = '0.0.0.0', port = 5075)
