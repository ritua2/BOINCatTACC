#!/usr/bin/env python3

"""
BASICS

Removes all stopped containers and images older than 4h. Designed to aboid filling the system's disk space with user's images.
Since user's will have already received their images in a tar file, no data will be lost.
Designed to be run as a cron job, but it can also be done manually
"""


import docker
import redis
import datetime
import sys



r = redis.Redis(host='0.0.0.0', port = 6389, db=2)
# Database for keeping deleted images and the time of doing so
r9 = redis.Redis(host='0.0.0.0', port = 6389, db=9)


client = docker.from_env()
image = client.images
container = client.containers


# Searches all the users only, no MIDAS directories
all_users = [x.decode('UTF-8') for x in r.keys() if ';' not in x.decode('UTF-8')]
all_images = [y.tags[0] for y in image.list()]


# Given an image name, finds if it is custom MIDAS or not
# IMTAG (str): Image tag
def MIDAS_image(IMTAG):

    for usnam in all_users:
        if usnam.lower().replace('@', '') in IMTAG:
            return True

    return False

# Obtains the time when an image was created
def Image_creation_time(IMTAG):

    ptim = image.get(IMTAG).attrs['Created'].replace("T", ' ').split('.')[0]

    return datetime.datetime.strptime(ptim, "%Y-%m-%d %H:%M:%S")


# Checks if an image was created more than 4 hours ago
# creation_time (datetime obj.): Time when the image was created
def image_older_4h(creation_time):

    if (datetime.datetime.utcnow() - creation_time).total_seconds() > (4*3600):
        return True

    return False

# [[Image Tag, Creation time], ...]
MIDAS_images = [[z, Image_creation_time(z)] for z in all_images if MIDAS_image(z)]

# Removes all exited containers
container.prune()

# Checks if there are any images due to be deleted
to_be_deleted = [w[0] for w in MIDAS_images if image_older_4h(w[1])]

if len(to_be_deleted) == 0:
    print("No new MIDAS images")
    sys.exit()


for imim in to_be_deleted:
    image.remove(image=imim, force=True)
    r9.set(imim, datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
