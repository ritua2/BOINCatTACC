#!/usr/bin/env python3

"""
BASICS


Returns a researcher's data in a JSON form
"""

import redis
from flask import Flask, jsonify
import preprocessing as pp


app = Flask(__name__)
r_data = redis.Redis(host='0.0.0.0', port=6389, db=0)
r_alloc = redis.Redis(host='0.0.0.0', port=6389, db=2)


@app.route("/boincserver/v2/api/user_data/personal/<toktok>")
def user_data(toktok):

    if pp.token_test(toktok) == False:
       return 'INVALID token'

    U_alloc = r_alloc.get(toktok).decode("UTF-8")

    # Finds all the data
    totjobs = r_data.llen("Token")

    U_data = []
    for qq in range(0, totjobs):
        if r_data.lindex("Token", qq).decode("UTF-8") == toktok:
            # [[Image, Command, Date (Sub), Date (Run), Notified], ..]
            U_data.append([])
            curdat = {}
            imnam = r_data.lindex("Image", qq).decode("UTF-8")
            if "carlosred/" != imnam[:10:]:
                imnam += " (CUSTOM)"
            curdat["Image"] = imnam
            curdat["Command"] = r_data.lindex("Command", qq).decode("UTF-8")
            curdat["Date (Sub)"] = r_data.lindex("Date (Sub)", qq).decode("UTF-8")
            curdat["Date (Run)"] = r_data.lindex("Date (Run)", qq).decode("UTF-8")
            curdat["Notified"] = r_data.lindex("Notified", qq).decode("UTF-8")
            U_data[-1].append(curdat)

    return jsonify({"allocation":U_alloc, "job data":U_data})



if __name__ == '__main__':
   app.run(host = '0.0.0.0', port = 5092)
