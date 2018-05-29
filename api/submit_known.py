"""
BASICS

Automated job submission for known Docker images through APIs
"""

import os
from flask import Flask
import preprocessing as pp


app = Flask(__name__)
UPLOAD_FOLDER = "../html/user/token_data/process_files"


@app.route("/boincserver/v2/submit_known/token=<toktok>", methods = ['GET', 'POST'])
def upload_file(toktok):
   
    if pp.token_test(toktok) == False:
       return 'Invalid token'
 
    if request.method != 'POST':
       return "Invalid. Submit a text file"    

    file = request.files['file']
    # Avoids empty files and non-text files
    if file.filename == '':
       return 'No file submitted'
    if file.filename.split('.')[-1] != 'txt':
       return "File type invalid, only text files are acccepted"

    # Randomizes the file name to avoid matches
    new_filename = pp.random_file_name()
    file.save(os.path.join(UPLOAD_FOLDER, new_filename))
    return "File submitted for processing"
    
    
if __name__ == '__main__':
   app.run(host = '0.0.0.0', port = 5075)
