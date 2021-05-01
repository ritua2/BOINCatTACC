#!/usr/bin/env python3

"""
BASICS

Returns user files or information about them
"""

import os, sys, shutil, requests
from flask import Flask, request, jsonify, send_file
import base_functions as bf
from werkzeug.utils import secure_filename


app = Flask(__name__)
REEF_FOLDER = os.environ['Reef_Path']+"/sandbox/"


# Checks if reef cloud storage is available
@app.route('/reef/status')
def api_operational():
    return 'External Reef cloud storage is available'


# Returns a string comma-separated, of all the files owned by a user
@app.route('/reef/all_user_files/<rkey>/<toktok>')
def all_user_files(toktok, rkey):

    if not bf.valid_key(rkey):
        return "INVALID key"
    AAA = []
    AAA,user = bf.get_user_files(toktok)

    if len(AAA)==0 and user==None:
        return "Sandbox not set-up, create a sandbox first"

    return ' '.join(AAA)

# Uploads one file
@app.route("/reef/upload/<rkey>/<toktok>", methods=['POST'])
def result_upload(toktok, rkey):

    if not bf.valid_key(rkey):
        return "INVALID key"

    # user must be added to the database beforehand
    if not bf.valid_user(toktok):
        return "INVALID user"

    if request.method != 'POST':
       return 'INVALID, no file submitted'

    file = request.files['file']
    fnam = request.form['filename']

    # Avoids empty filenames and those with commas
    if fnam == '':
       return 'INVALID, no file uploaded'
    if ',' in fnam:
       return "INVALID, no ',' allowed in filenames"
    
    # delete file with the same name if already exist
    new_name = secure_filename(fnam)
    filevm,vmkey=bf.get_file_vm(toktok,new_name,'')
    if filevm != None and vmkey != None:
        delete = requests.get("https://"+filevm+":3443/reef/storage_delete_file/"+vmkey+"/"+toktok+"/"+new_name, verify=False) # https with selsigned certs
        #delete = requests.get("https://"+filevm+":3443/reef/storage_delete_file/"+vmkey+"/"+toktok+"/"+new_name) # https
	#delete = requests.get("http://"+filevm+":3443/reef/storage_delete_file/"+vmkey+"/"+toktok+"/"+new_name) #http
    
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

    #req = requests.post("https://"+ip+":3443"+"/reef/storage_upload/"+key+"/"+toktok, files=files)  # https
    req = requests.post("https://"+ip+":3443"+"/reef/storage_upload/"+key+"/"+toktok, files=files, verify=False)  # https with self signed certs
    #req = requests.post("http://"+ip+":3443"+"/reef/storage_upload/"+key+"/"+toktok, files=files) #http

    # remove the file from local storage    
    if os.path.exists(os.path.join(UPLOAD_DIR, new_name)):
        os.remove(os.path.join(UPLOAD_DIR, new_name))  

    return req.text


# Deletes a file already present in the user
@app.route('/reef/delete_file/<rkey>/<toktok>/<FILE>')
def delete_user_file(toktok, rkey, FILE):

    if not bf.valid_key(rkey):
        return "INVALID key"

    # user must be added to the database beforehand
    if not bf.valid_user(toktok):
        return "INVALID user"

    vmip,nkey = bf.get_file_vm(toktok,FILE,'')
    if vmip == None or nkey == None:
        return "INVALID, file not found"
    #req = requests.get("https://"+vmip+":3443"+"/reef/storage_delete_file/"+nkey+"/"+toktok+"/"+FILE)  # https
    req = requests.get("https://"+vmip+":3443"+"/reef/storage_delete_file/"+nkey+"/"+toktok+"/"+FILE, verify=False)  # https with self signed certs
    #req = requests.get("http://"+vmip+":3443"+"/reef/storage_delete_file/"+nkey+"/"+toktok+"/"+FILE) # http

    return req.text

# Returns a file
@app.route('/reef/reef/<rkey>/<toktok>/<FIL>')
def results_file(rkey, toktok, FIL):

    if not bf.valid_key(rkey):
        return "INVALID key"

    # user must be added to the database beforehand
    if not bf.valid_user(toktok):
        return "INVALID user"

    vmip,nkey = bf.get_file_vm(toktok,FIL,'')
    if vmip == None or nkey == None:
        return "INVALID, File not found"
    #req = requests.get("https://"+vmip+":3443"+"/reef/storage_reef/"+nkey+"/"+toktok+"/"+FIL)  # https
    req = requests.get("https://"+vmip+":3443"+"/reef/storage_reef/"+nkey+"/"+toktok+"/"+FIL, verify=False)  # https with self signed certs
    #req = requests.get("http://"+vmip+":3443"+"/reef/storage_reef/"+nkey+"/"+toktok+"/"+FIL) # http

    if "INVALID" in req.text and len(req.text)<40:
        return req.text

    USER_DIR=REEF_FOLDER+'DIR_'+str(toktok)+'/download/'
    if not os.path.exists(USER_DIR):
        os.makedirs(USER_DIR)

    open(USER_DIR+FIL,'wb').write(req.content)
    return send_file(USER_DIR+str(FIL))

if __name__ == '__main__':
   app.run(host ='0.0.0.0', port = 2000)
