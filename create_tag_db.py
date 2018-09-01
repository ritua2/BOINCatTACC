"""
BASICS

Creates the tag database for BOINC jobs
This program must only be run once; if more keys are needed, the system will automatically update
"""

import sys
import redis
from api.topics import all_tags as at





r = redis.Redis(host='0.0.0.0', port=6389, db=12)


# Adds the TACC-supported images to the database
try:
    r.delete('Known Images')
except:
    pass


# Records the Image tags
IMTAGS = {}

for IM in at.TACCIM.keys():
    # Easier to track images if they are in a database
    r.rpush('Known Images', IM)

    # Assigns each image to a topic
    # A single image can have multiple topics
    # Mostly useful for non-TACC images

    # IMTAGS = {major:[[Image 1, Image 2, ...], {minor 1, minor 2, ...}]}

    for major in at.TACCIM[IM].keys():
        if major not in IMTAGS.keys():
            IMTAGS[major] = [[IM], {}]
        else:
            IMTAGS[major][0].append(IM)

        # Adds the minors
        for minor in at.TACCIM[IM][major]:
            if minor not in IMTAGS[major][1].keys():
                IMTAGS[major][1][minor] = [[IM], {}]
            else:
                IMTAGS[major][1][minor][0].append(IM)


# Each topic (tag) can have subtags of its own, as well as a count of jobs left and a count of completed jobs
for major in at.tags.keys():
    A = at.tags[major]
    B = {}
    for minor in A:
        B[minor] = {}
        B[minor]["Jobs Completed"] = []
        B[minor]["Jobs Available"] = []
        try:
            B[minor]["Images"] = IMTAGS[major][1][minor][0]
        except:    
            B[minor]["Images"] = []

    B["Jobs Completed"] = []
    B["Jobs Available"] = []
    try:
        B["Images"] = IMTAGS[major][0]
    except:
        B["Images"] = []

    r.hmset(major, B)
