"""
BASICS


Interactions with VolCon mirrors
"""


import mysql_interactions as mints
import os
import random
import redis
import requests


r = redis.Redis(host = '0.0.0.0', port = 6389, db = 3)



# Chooses a random mirror
# Returns the IP
def get_random_mirror():

    K = [H.decode("UTF-8") for H in r.hkeys("VolCon")]
    H = [h for h in K if "M-"==h[:2]]
    random.shuffle(H)

    return H[0][2:]



# Returns the key of random mirror
def mirror_key(mirror_IP):
    return r.hget("M-"+mirror_IP, "disconnect-key").decode("UTF-8")



# Uploads job information to a random mirror, only valid for TACC or public images
# User may provide any information except the key
# JOB_INFO (dict): Contains any infromation about the job

def upload_job_to_mirror(JOB_INFO):

    mirror_ip = get_random_mirror()

    JOB_INFO["key"] = mirror_key(get_random_mirror())
    mints.update_mirror_ip(JOB_INFO["VolCon_ID"], mirror_ip)
    # Updates result to mirror
    requests.post('http://'+mirror_ip+":7000/volcon/mirror/v2/api/public/receive_job_files",
        json=JOB_INFO)


# Uploads a certain file to a mirror
# full_file_path(str): Full path to file
# mirror_ip (str)
# volcon_id (str)
def upload_file_to_mirror(full_file_path, mirror_ip, volcon_id):
    requests.post('http://'+mirror_ip+":7000/volcon/mirror/v2/api/MIDAS/receive_files/"+volcon_id+"/key="+mirror_key(mirror_ip),
                        files={"file": open(full_file_path,"rb")})



# Uploads a set of files to a mirror and the job information
def MIDAS_job_to_mirror(JOB_INFO, fileset):
    pass

