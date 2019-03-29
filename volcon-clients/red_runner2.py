#!/usr/bin/env python3

"""
BASICS

Reads the Redis database and submits the jobs that have not been done yet to
the adtd-p waiting list.
Each job becomes represented by a Redis hash containing all the necessary information.
This information is also represented in a JSON file in the same format
"""

import redis
import docker
import json
import datetime
import subprocess as sp
import os, shutil
import hashlib
import tarfile

r = redis.Redis(host = '0.0.0.0', port = 6389, db =0)
r_adtd = redis.Redis(host = '0.0.0.0', port = 6389, db =14)
TASKS_FOLDER = "/home/boincadm/project/adtd-protocol/tasks/"
client = docker.from_env(timeout=5*60)
image = client.images

# Loops through the database and sees the jobs that have not been run yet

for qq in range(0, r.llen('Token')):
    
    # The time run is set to 0 for jobs not yet run
    if r.lindex('Date (Run)', qq).decode('UTF-8') == 'ADTD':

      # Obtains the time of last modification
      prestime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      # Submits the job to the boinc2server app
      # Database stores the results in bytes, must be decoded into standard strings
      acim = r.lindex('Image', qq).decode('UTF-8')
      accom = r.lindex('Command', qq).decode('UTF-8')
      identity = hashlib.sha256(str(datetime.datetime.now()).encode('UTF-8')).hexdigest()[:16:]
      gpu_needed = False


      if "nvcc" in accom:
        gpu_needed = True


      # JSON Data
      data = {"Image":acim, "Command":accom, "Results":"/root/shared/results", "ID":identity, "Error":"Not Run", 
              "Processed":prestime, "GPU":gpu_needed}

      # Checks if the image is on the server, if not, it downloads it from dockerhub
      all_images = [y.tags[0] for y in image.list()]
      if acim not in all_images:
        try:
            image.pull(acim)
        except:
            r.lset('Error', qq, identity+' | ERROR, Image does not exist')
            r.lset('Date (Run)', qq, ' | ERROR, Image does not exist')
            continue

      # Saves the image into a tar file and tars the data with it
      r.lset('Date (Run)', qq, 'ADTD (Ready)')
      img = image.get(acim)
      try:
        resp = img.save()
      except:
        r.lset('Error', qq, identity+' | ERROR, Image cannot be used due to large size')
        r.lset('Date (Run)', qq, ' | ERROR, Image cannot be used due to large size')
        continue        
      os.mkdir(TASKS_FOLDER+identity)
      os.chdir(TASKS_FOLDER+identity)
      ff = open(TASKS_FOLDER+identity+"/image.tar.gz", 'wb')
      for salmon in resp:
          ff.write(salmon)
      ff.close()
      with open(TASKS_FOLDER+identity+"/adtdp.json", 'w') as outfile:
           json.dump(data, outfile)

      with tarfile.open(TASKS_FOLDER+identity+"/tbp.tar.gz", "w:gz") as tar:
          tar.add("image.tar.gz")
          tar.add("adtdp.json")

      r_adtd.hmset(identity, data)
      r.lset('Error', qq, identity)
