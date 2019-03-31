"""
BASICS

Executes the VolCon jobs in independent docker containers
"""


import docker 
import os
import requests



cluster = os.environ["cluster"]
cluster_key = os.environ["cluster_key"]
dk = os.environ["disconnect_key"]
GPU = os.environ["GPU"]
main_server = os.environ["main_server"]




# Requests a job given a priority
# Returns [Mirror IP, VolCon-ID]
def request_job(priority_level):

    r = requests.post('http://'+os.environ["main_server"]+":5091/volcon/v2/api/jobs/request",
        json={"cluster": cluster, "disconnect-key":dk, "GPU":GPU, "priority-level":priority_level})


