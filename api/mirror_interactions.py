"""
BASICS


Interactions with VolCon mirrors
"""


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
    return r.hget("M-"+mirror_IP, "disconnect-key")



# Uploads job information to a random mirror, only valid for TACC or public images
# User may provide any information except the key
# JOB_INFO (dict): Contains any infromation about the job

def upload_job_to_mirror(JOB_INFO):

    JOB_INFO["key"] = mirror_key(get_random_mirror())

    r = requests.post('http://'+os.environ["main_server"]+":5089/volcon/v2/api/mirrors/status/update",
        json=JOB_INFO)




