#!/usr/bin/env python3


"""
BASICS


MIDAS: Multiple Input Docker Automation System

Generates a github image with all user commands inside to be submitted to BOINC
"""

from flask import Flask, request, jsonify
import tarfile, shutil, os, sys
import preprocessing as pp
from midas_processing import midas_reader as mdr
from werkzeug.utils import secure_filename
import redis


import mysql_interactions as mints



r = redis.Redis(host = '0.0.0.0', port = 6389, db=2)
app = Flask(__name__)
UPLOAD_FOLDER = "/home/boincadm/project/api/sandbox_files"


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
    'Disclaimer': 'API usage is restricted to users with granted access, Token required. To test token, curl ->http://{BOINC_IP}:5000/boincserver/test_token=ENTER_TOKEN',
    'User guide': {'Steps': 'Submit a tar.gz file containing a compressed folder with all the files. File must be a tar.gz , all other inputs will not be accepted .',
                   'Contents' : 'All files must contain a README.txt (file ending MUST be .txt, all other inputs will not be accepted',
                   'README.txt': 'Follow instructions, curl -> http://SERVER_IP/boincserver/README_MIDAS_example.txt',

                   'Other files': 'Their number and name must be accounted for in the README',
                   'Outputs': 'Their full path must be included'            

                  },
                  
    'Limitations': 'MIDAS is based on Docker publicly available Docker images. As such, only open-source, free to use software is allowed. No Intel compilers, software that requires key access, enterprise editions, or private OS (Windows, Mac are not allowed)',
    'Supported Languages': 'python3, C, C++, C++ cget, R, bash, Fortran',
    'Supported OS': 'Ubuntu 16.04',

    'Root Access': 'Assume root access when installing dependencies trough a bash script'

    }

    return jsonify(full)


# Allows the user to see how much space is still available in his allocation
# Allows to check the user's allocation status
@app.route('/boincserver/v2/midas_allocation_status/token=<toktok>')
def reef_allocation_status(toktok):
    if pp.token_test(toktok) == False:
       return 'Invalid token'
    used_space = pp.user_sandbox_size(str(toktok))/1073741824
    assigned_allocation = r.get(toktok).decode('UTF-8')
    all_info = {'Max. allocation': assigned_allocation+' GB',
                'Used space': str(used_space)+' GB', 
                'Space available left': str((1 - used_space/float(assigned_allocation))*100)+'% allocation available'}

    return jsonify(all_info)


# Returns a list of all images owned by the user, as well as their size
@app.route("/boincserver/v2/midas/user_images/token=<toktok>")
def user_images(toktok):
    if not pp.token_test(toktok):
       return 'Invalid token'

    user_images = {}

    for IMAGE in client.images.list():
        try:
            NAME = IMAGE.attrs['RepoTags'][0]
        except:
            continue
        if NAME.split(':')[0] == toktok.lower():
          user_images[NAME] = str(IMAGE.attrs['Size']/(10**9))+" GB"

    return jsonify(user_images)


# Allows the user to delete an image
# Allows the user to provide both the name and tag, or just the tag
# After an image is deleted, the user's recovers its equivalent memory back into his allocation
@app.route("/boincserver/v2/midas/delete_image/token=<toktok>", methods = ['GET', 'POST'])
def delete_image(toktok):
    if not pp.token_test(toktok):
       return 'Invalid token'
    if request.method != 'POST':
      return 'Invalid, provide an image to be deleted'

    UTOK = str(toktok).lower()
    DATA = str(request.form['del'])
    IMTAG = DATA

    if ':' not in DATA:
        IMTAG = UTOK.lower()+':'+DATA

    try:
        
        r.incrbyfloat(toktok, float(client.images.get(IMTAG).attrs['Size'])/(10**9))
        client.images.remove(image=IMTAG, force=True)
        return 'User image has been deleted. User allocation is now '+r.get(toktok).decode('UTF-8')+" GB"

    except:
        return 'ERROR: Image does not exist or is not owned by user'


# Returns all the OS and language references
@app.route("/boincserver/v2/references/midas/token=<toktok>")
def references(toktok):
    if  pp.token_test(toktok) == False:
        return 'Invalid token'
    allref = {'OS':{'Ubuntu 16.04':'Ubuntu_16.04'},
              'Languages':{'python2':'Not supported', 'python3':'python, python3', 'Go':'Go', 'R':'R', 'Fortran':'Fortran90', 'C':'C', 'C++':'C++'}
             }
    return jsonify(allref)


# Gets the user a list of all MIDAS directories
@app.route("/boincserver/v2/dirs/midas/token=<toktok>")
def dirs_midas(toktok):
    if  pp.token_test(toktok) == False:
        return 'Invalid token'
    
    midas_dirs = [x for x in os.listdir('/home/boincadm/project/api/sandbox_files/DIR_'+str(toktok)) if 'MID_'==x[:4:]]
    return ', '.join(midas_dirs)


# Allows the user to delete a MIDAS directory with all the files it contains, irreversible
@app.route("/boincserver/v2/delete_midas_dir/token=<toktok>", methods = ['GET', 'POST'])
def delete_midas_dir(toktok):
    if  pp.token_test(toktok) == False:
        return 'Invalid token'
    if request.method != 'POST':
      return 'Invalid, provide a file to be deleted'

    # Accounts for missing directories
    if str('DIR_'+toktok) not in os.listdir('/home/boincadm/project/api/sandbox_files'):
       return 'User directory does not exist'
    try: 
       MIDIR = request.form['del']    
       if MIDIR == '':    
          return 'No file provided'     
       shutil.rmtree('/home/boincadm/project/api/sandbox_files/DIR_'+str(toktok)+'/'+str(MIDIR))
       return 'Midas directory deleted'

    except:
       return 'MIDAS directory does not exist'


# Uploads a file for further MIDAS processing
@app.route('/boincserver/v2/midas/token=<toktok>/username=<Username>', methods = ['GET', 'POST'])
def midas(toktok, Username):

    if  pp.token_test(toktok) == False:
        return 'Invalid token'
    
    if request.method != 'POST':
        return 'Invalid, no file submitted'

    file = request.files['file']

    try:
       ALL_USER_DATA = os.listdir('/home/boincadm/project/api/sandbox_files/DIR_'+str(toktok))
    except:
       return 'User sandbox is not set-up, create a sandbox first'

    # If no app is provided, it will assume BOINC
    try:
        boapp = request.form["app"].lower()
        if (boapp != "boinc2docker") and (boapp != "volcon"):
            return "INVALID app"
    except:
        boapp = "boinc2docker"
    
    # No user can submit jobs with a full allocation
    assigned_allocation = float(r.get(toktok).decode('UTF-8'))

    if pp.user_sandbox_size(str(toktok)) > (assigned_allocation*1073741824):
        return 'User has exceded asssigned allocation. Current available allocation is '+str(assigned_allocation)+' GB'

    if file.filename == '':
        return 'Invalid, no file uploaded'
    if ',' in file.filename:
        return "ERROR: No ',' allowed in filenames"
    if ('.tar.gz' not in file.filename) and ('.tgz' not in file.filename):
        return 'ERROR: Compression file not accepted, file must be .tgz or .tar.gz'


    new_name = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER+'/DIR_'+str(toktok), new_name))
    try:
        TAR = tarfile.open(UPLOAD_FOLDER+'/DIR_'+str(toktok)+'/'+new_name)
    except:
        return 'ERROR: python cannot open tar file'
    if not any('README.txt' in str(f) for f in TAR.getmembers()):
        os.remove(os.path.join(UPLOAD_FOLDER+'/DIR_'+str(toktok), new_name))
        return 'ERROR: tar file does not contain mandatory README.txt'

    # Creates a new MIDAS directory with a new name
    while True:
        new_MID = 'MID_'+pp.random_dir_name()
        if new_MID not in ALL_USER_DATA: break


    # Checks the README for all necessary inputs
    TAR_PATH = UPLOAD_FOLDER+'/DIR_'+str(toktok)+'/'+new_MID
    os.makedirs(TAR_PATH)
    TAR.extractall(TAR_PATH)

    if not mdr.valid_README(TAR_PATH+'/README.txt'):
        shutil.rmtree('/home/boincadm/project/api/sandbox_files/DIR_'+str(toktok)+'/'+new_MID)
        return 'ERROR: README is not valid'

    if not mdr.valid_OS(TAR_PATH+'/README.txt'):
        shutil.rmtree('/home/boincadm/project/api/sandbox_files/DIR_'+str(toktok)+'/'+new_MID)
        return 'ERROR: OS is not accepted'
        
    if not mdr.present_input_files(TAR_PATH):
        shutil.rmtree('/home/boincadm/project/api/sandbox_files/DIR_'+str(toktok)+'/'+new_MID)
        return 'ERROR: Not all input files for commands are present'

    if not mdr.valid_language(TAR_PATH+'/README.txt'):
        shutil.rmtree('/home/boincadm/project/api/sandbox_files/DIR_'+str(toktok)+'/'+new_MID)
        return 'ERROR: Language is not accepted'

    # Avoids cases where no libraries are needed at all
    if (not mdr.install_libraries(TAR_PATH+'/README.txt')) and (mdr.install_libraries(TAR_PATH+'/README.txt') != []):
        shutil.rmtree('/home/boincadm/project/api/sandbox_files/DIR_'+str(toktok)+'/'+new_MID)
        return 'ERROR: Language does not support libraries'


    # Creates a redis database with syntax {TOKEN;MID_DIRECTORY:boapp}
    r.set(toktok+';'+new_MID, boapp)


    # Obtains the commands to run
    ALL_COMS = mdr.present_input_files(TAR_PATH)
    FINAL_COMMANDS = []
    for acom in ALL_COMS:

        # Other languages
        FINAL_COMMANDS.append(mdr.execute_command(acom))

    complete_command = ";".join(FINAL_COMMANDS)


    # Adds tags to database
    # STEM is always assumed
    tags_used = "STEM"
    mints.add_MIDAS_job(Username, toktok, tags_used, new_MID, complete_command, boapp, "cli", "MIDAS ready")

    return 'File submitted for processing'



if __name__ == '__main__':
   app.run(host ='0.0.0.0', port = 5085, debug=False, threaded=True)
