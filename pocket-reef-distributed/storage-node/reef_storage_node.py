#!/usr/bin/env python3
"""

BASICS

Implements communication between end user calling greyfish and the other nodes
"""


from flask import Flask, request, send_file
from werkzeug.utils import secure_filename
import os, shutil, requests, tarfile, traceback
import base_functions as bf

app = Flask(__name__)
REEF_FOLDER = "/rdat/sandbox/"
URL_BASE = os.environ["URL_BASE"]
CURDIR = dir_path = os.path.dirname(os.path.realpath(__file__))

#################################
# FILE ACTIONS
#################################

# Uploads one file
# Directories must be separated by ++
@app.route("/reef/storage_upload/<nkey>/<toktok>", methods=['POST'], defaults={'DIR':''})
@app.route("/reef/storage_upload/<nkey>/<toktok>/<DIR>", methods=['POST'])

def result_upload(nkey,toktok,DIR=''):    
    if not nkey == os.environ['NODE_KEY']:
        return "INVALID node key"

    if str('DIR_'+toktok) not in os.listdir(REEF_FOLDER):
        os.makedirs(REEF_FOLDER+'DIR_'+str(toktok))

    file = request.files['file']
    fnam = file.filename

    # Ensures no commands within the filename
    new_name = secure_filename(fnam)

    if not os.path.exists(REEF_FOLDER+'DIR_'+str(toktok)+'/'+'/'.join(DIR.split('++'))):
        os.makedirs(REEF_FOLDER+'DIR_'+str(toktok)+'/'+'/'.join(DIR.split('++')))

    file.save(os.path.join(REEF_FOLDER+'DIR_'+str(toktok)+'/'+'/'.join(DIR.split('++')), new_name))
    #res = requests.get("https://"+URL_BASE+":2003/reef/cluster/whoami")
    res = requests.get("https://"+URL_BASE+":2003/reef/cluster/whoami", verify=False)
    #res = requests.get("http://"+URL_BASE+":2003/reef/cluster/whoami")

    ip = res.text
    try:
        for root, dirs, files in os.walk(REEF_FOLDER+'DIR_'+str(toktok)+'/'):
            bf.add_dir(ip,toktok,'++'.join(root.replace(REEF_FOLDER+'DIR_'+str(toktok)+'/','').split('/')))
            for file in files:
                bf.add_file(ip,toktok,'++'.join(root.replace(REEF_FOLDER+'DIR_'+str(toktok)+'/','').split('/')),file)

    except:
        traceback.print_exc()
        return "INVALID,  can't update database"
    bf.update_node_space(ip)
    return 'File succesfully uploaded to Reef'

# Deletes a file already present in the user
@app.route('/reef/storage_delete_file/<nkey>/<toktok>/<FILE>', defaults={'DIR':''})
@app.route('/reef/storage_delete_file/<nkey>/<toktok>/<FILE>/<DIR>')
def delete_file(toktok, nkey, FILE, DIR=''):
    if not nkey == os.environ['NODE_KEY']:
        return "INVALID node key"

    if str('DIR_'+toktok) not in os.listdir(REEF_FOLDER):
       return 'INVALID, User directory does not exist'

    try:
        #res = requests.get("https://"+URL_BASE+":2003/reef/cluster/whoami")
        res = requests.get("https://"+URL_BASE+":2003/reef/cluster/whoami", verify=False)
        #res = requests.get("http://"+URL_BASE+":2003/reef/cluster/whoami")
        ip = res.text
        bf.remove_file(ip,toktok,DIR,FILE)
        os.remove(REEF_FOLDER+'DIR_'+str(toktok)+'/'+'/'.join(DIR.split('++'))+'/'+str(FILE))
        bf.update_node_space(ip)
        return 'File succesfully deleted from Reef storage'
    except:
        traceback.print_exc()
        return 'INVALID, File is not present in Reef'

# Returns a file
@app.route("/reef/storage_reef/<nkey>/<toktok>/<FIL>", defaults={'DIR':''})
@app.route('/reef/storage_reef/<nkey>/<toktok>/<FIL>/<DIR>')
def grey_file(nkey, toktok, FIL, DIR=''):
    if not nkey == os.environ['NODE_KEY']:
        return "INVALID node key"

    if str('DIR_'+toktok) not in os.listdir(REEF_FOLDER):
       return 'INVALID, User directory does not exist'

    USER_DIR = REEF_FOLDER+'DIR_'+str(toktok)+'/'+'/'.join(DIR.split('++'))
    if str(FIL) not in os.listdir(USER_DIR):
       return 'INVALID, File not available'

    return send_file(os.path.join(USER_DIR, str(FIL)), as_attachment=True)

if __name__ == '__main__':
   app.run()
