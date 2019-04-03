"""
BASICS

Closes the container if the correct disconnect key is received
"""



from flask import Flask, request, jsonify
import json
import os
import threading
import time



app = Flask(__name__)



# Writes the disconnect key to a dile, signaling the container to kill the main processing, effectively kiling itself
def kill_container():

    time.sleep(2) # Waits 2 s to wait for the call being written
    with open("/client/disconnect.txt", "w") as ff:
        ff.write(os.environ["disconnect_key"])



# Modifies priority file
def new_priorities(newp):

    with open("/client/priorities.json", "w") as ff:
        ff.write(json.dumps(newp))


@app.route('/volcon/client/api/close/<disconnect_key>', methods=['GET'])
def close(disconnect_key):

    if disconnect_key == os.environ["disconnect_key"]:
        t = threading.Thread(target=kill_container)
        t.start()
        return "System is being disconnected now"
    else:
        return "Incorrect disconnect key"



# Returns a copy of the priority list
@app.route('/volcon/client/api/priorities/<disconnect_key>', methods=['GET'])
def show_priorities(disconnect_key):

    if not disconnect_key == os.environ["disconnect_key"]:
        return "Incorrect key"

    with open("/client/priorities.json", "r") as ff:
        current = json.load(ff)

    return "Current priorities in order: "+", ".join(current["available-priorities"])



# Adds or removes what kind of priority can the system execute
# Does not account for race conditions, expected to be done very rarely
# Note: If a priority is repeated in the list, it needs to be removed as many times as there are mentions of it
@app.route('/volcon/client/api/priorities/change/<change>/<talkedabout>/<disconnect_key>', methods=['GET'])
def change_priorities(disconnect_key, change, talkedabout):

    if not disconnect_key == os.environ["disconnect_key"]:
        return "Incorrect key"

    with open("/client/priorities.json", "r") as ff:
        current = json.load(ff)

    if change == "append":
        current["available-priorities"].append(talkedabout)

        # Modifies the file
        new_priorities(current)
        return "Current priorities in order: "+", ".join(current["available-priorities"])

    if change == "remove":
        try:
            current["available-priorities"].remove(talkedabout)
        except:
            return "'"+talkedabout+"' is not a priority"

        # Modifies the file
        new_priorities(current)
        return "Current priorities in order: "+", ".join(current["available-priorities"])


    return "INVALID change, only options are 'append', 'remove'"




app.run(host = '0.0.0.0', port = 8000, debug=False, threaded=True)

