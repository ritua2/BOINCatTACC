#!/usr/bin/env python3

"""
BASICS

Returns a results file
Different port because of how common it is
"""

import os, shutil, requests
from flask import Flask, send_file, request
import base_functions as bf
from werkzeug.utils import secure_filename

app = Flask(__name__)
REEF_FOLDER = os.environ['Reef_Path']+"/sandbox/"


# Returns a results file
@app.route('/reef/results/<rkey>/<toktok>/<FIL>')
def results_file(rkey, toktok, FIL):

    if not bf.valid_key(rkey):
        return "INVALID key"

    # user must be added to the database beforehand
    if not bf.valid_user(toktok):
        return "INVALID user"
    
    DIR='___RESULTS'
    vmip,nkey = bf.get_file_vm(toktok,FIL,DIR)
    if vmip == None or nkey == None:
        return "INVALID, File not found"
    #req = requests.get("https://"+vmip+":3443"+"/reef/storage_reef/"+nkey+"/"+toktok+"/"+FIL+"/"+DIR) # https
    req = requests.get("https://"+vmip+":3443"+"/reef/storage_reef/"+nkey+"/"+toktok+"/"+FIL+"/"+DIR, verify=False) # https with self signed certificate
    #req = requests.get("http://"+vmip+":3443"+"/reef/storage_reef/"+nkey+"/"+toktok+"/"+FIL+"/"+DIR) # http

    if "INVALID" in req.text and len(req.text)<40:
        return req.text
    
    USER_DIR=REEF_FOLDER+'DIR_'+str(toktok)+'/download/'
    if not os.path.exists(USER_DIR):
        os.makedirs(USER_DIR)

    open(USER_DIR+FIL,'wb').write(req.content)
    return send_file(USER_DIR+str(FIL))


# Returns a space-separated list of all files a user has in results
@app.route("/reef/results_all/<rkey>/<toktok>")
def reef_results_all(toktok, rkey):

    if not bf.valid_key(rkey):
        return "INVALID key"

    AAA = [] 
    AAA,user = bf.get_user_files(toktok,'___RESULTS')

    if len(AAA)==0 and user==None:
        return 'Sandbox not set-up, create a sandbox first'

    # Returns the results (space-separated)
    return ' '.join(AAA)


# Uploads one file to the results folder
@app.route("/reef/result_upload/<rkey>/<toktok>", methods=['POST'])
def result_upload(toktok, rkey):
    if not bf.valid_key(rkey):
        return "INVALID key"

    # user must be added to the database beforehand
    if not bf.valid_user(toktok):
        return "INVALID user"

    if request.method != 'POST':
       return 'INVALID, no file submitted'

    file = request.files['file']

    # Avoids empty filenames and those with commas
    if file.filename == '':
       return 'INVALID, no file uploaded'
    if ',' in file.filename:
       return "INVALID, no ',' allowed in filenames"

    # delete file with the same name if already exist
    new_name = secure_filename(file.filename)
    filevm,vmkey=bf.get_file_vm(toktok,new_name,'___RESULTS')
    if filevm != None and vmkey != None:
        #delete = requests.get("https://"+filevm+":3443/reef/storage_delete_file/"+vmkey+"/"+toktok+"/"+new_name+"/___RESULTS") # https
        delete = requests.get("https://"+filevm+":3443/reef/storage_delete_file/"+vmkey+"/"+toktok+"/"+new_name+"/___RESULTS", verify=False)# https with self signed certificate
        #delete = requests.get("http://"+filevm+":3443/reef/storage_delete_file/"+vmkey+"/"+toktok+"/"+new_name+"/___RESULTS") # http

    #save file locally
    UPLOAD_DIR = REEF_FOLDER+'DIR_'+str(toktok)+'/upload'
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    file.save(os.path.join(UPLOAD_DIR, new_name))

    # find VM that can fit the file
    filesize = os.stat(os.path.join(UPLOAD_DIR, new_name)).st_size
    vmip, nkey = bf.get_available_vms(filesize)
    if len(vmip)==0 or len(nkey)==0:
        os.remove(os.path.join(UPLOAD_DIR, new_name))
        return "Couldn't find any VM which can fit the file to be uploaded"

    ip=vmip[0]
    key=nkey[0]

    # upload the file to the first available VM
    files = {'file': open(os.path.join(UPLOAD_DIR, new_name), 'rb')}
    #req = requests.post("https://"+ip+":3443"+"/reef/storage_upload/"+key+"/"+toktok+"/___RESULTS", files=files) # https
    req = requests.post("https://"+ip+":3443"+"/reef/storage_upload/"+key+"/"+toktok+"/___RESULTS", files=files, verify=False) # https with self signed certificate
    #req = requests.post("http://"+ip+":3443"+"/reef/storage_upload/"+key+"/"+toktok+"/___RESULTS", files=files) # http

    # remove the file from local storage    
    if os.path.exists(os.path.join(UPLOAD_DIR, new_name)):
        os.remove(os.path.join(UPLOAD_DIR, new_name))

    return req.text


if __name__ == '__main__':
   app.run(host ='0.0.0.0', port = 2001)
