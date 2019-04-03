"""
BASICS

Executes the VolCon jobs in independent docker containers
"""


import datetime
import docker 
import json
import os
import requests
import sys
import time



cluster = os.environ["cluster"]
cluster_key = os.environ["cluster_key"]
dk = os.environ["disconnect_key"]
GPU = os.environ["GPU"]
main_server = os.environ["main_server"]
processes = int(os.environ["np"])
only_public = os.environ["only_public"]

# Max 5 minutes timeout for any job trying to load an image
image = docker.from_env(timeout=5*60).images
container =  docker.from_env().containers




# Requests a job given a priority
# Returns [Mirror IP, VolCon-ID]
def request_job(priority_level):

    r = requests.post('http://'+os.environ["main_server"]+":5091/volcon/v2/api/jobs/request",
        json={"cluster": cluster, "disconnect-key":dk, "GPU":GPU, "priority-level":priority_level, "public":only_public})
    return json.loads(r.text)



# Given a JSON object with the VolCon information, it calls the respective mirror and retrieves the information in a JSON format
# Only valid for public images (not MIDAS)
def get_mirror_info_public(jinfo):

    mirror_IP = jinfo["mirror-IP"]
    VolCon_ID = jinfo["VolCon-ID"]
    r = requests.get('http://'+mirror_IP+":7000/volcon/mirror/v2/api/public/request_job/"+VolCon_ID)

    # Returns False if its credentials are invalid
    try:
        A = json.loads(r.text)
        return A
    except:
        return r.text



# Runs a public image (TACC or not) job
# Based on the server information, runs the job
# previous_download_time (float): Time in seconds, for the previous steps
def run_in_container(job_info, previous_download_time):

    prestime = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    GPU_job = job_info["GPU"]
    Image = job_info["Image"]
    Command = job_info["Command"]
    TACC = job_info["TACC"]
    VolCon_ID = job_info["VolCon_ID"]

    if GPU:
        executer = "nvidia"
    else:
        executer = None

    # Chooses the results directory
    # Set as BOINC default if no more information is provided
    if "results-directory" in job_info.keys():
        results_dir = job_info["results-directory"]
    else:
        results_dir = "/root/shared/results"

    # Runs the container detached
    try:
        d1 = time.time()
        CONTAINER = container.run(image=Image, command="sleep infinity", detach=True, runtime=executer)
        d2 = time.time()

    except:
        Con_Data = {"date (Run)":prestime, "VolCon-ID":VolCon_ID, "Error":"Container failed to start"}
        # Notifies server
        # TODO TODO TODO



        return None

    # Filters the commands into an usable form
    CC = Command.replace("/bin/bash -c \"", "").replace("\"", "").split("; ")
    Report = {"date (Run)":prestime, "VolCon-ID":VolCon_ID, "download time":(d2-d1+previous_download_time)}

    # Returns the exit code
    comres = [[], []]
    start_time = time.time()
    for command in CC:
        try:
            RESP = CONTAINER.exec_run("/bin/bash -c \""+command+"\"")
            # Checks the exit code
            if RESP[0] != 0:
                raise

            comres[0].append(command)
            comres[1].append("Success")
        except:
            comres[0].append(command)
            comres[1].append("Error")

    Report["Commands"] = comres

    # Retrieves the result files
    # Opens it into a random name tar.gz that will be deleted later
    tarname = VolCon_ID+".tar"

    try:
        with open(tarname, "wb") as tarta:
            RESRES = CONTAINER.get_archive(path=results_dir)
            for bitbit in RESRES[0]:
                tarta.write(bitbit)
        Report["Result Error"] = "0"
    except:
        Report["Result Error"] = "Results directory does not exist"
        # Notify the server of the error
        requests.post('http://'+os.environ["main_server"]+":5091/volcon/v2/api/jobs/upload/report",
            json=Report)

        os.remove(tarname)
        CONTAINER.remove(force = True)
        container.prune()
        if not TACC:
            image.remove(Image, force = False)

        return None

    end_time = time.time()
    completed_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    Report["computation time"] = end_time-start_time

    # Tries to contact the server
    try:

        # Uploads result files
        requests.post('http://'+os.environ["main_server"]+":5091/volcon/v2/api/jobs/results/upload/"+VolCon_ID,
                    files={"file": open(VolCon_ID+".tar","rb")})

        # Uploads finishes job notification
        requests.post('http://'+os.environ["main_server"]+":5091/volcon/v2/api/jobs/upload/report",
                    json=Report)
    except:
        # The server has been disconnected
        pass



    # Kills the container and removes it
    os.remove(tarname)
    CONTAINER.kill()
    CONTAINER.remove(force = True)
    container.prune()

    # If the image is not TACC, it removes it
    if not TACC:
        image.remove(Image, force = False)



# Complete process function, including priority search







# Multiple processes


