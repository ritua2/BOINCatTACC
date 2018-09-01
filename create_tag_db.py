"""
BASICS

Creates the tag database for BOINC jobs
This program must only be run once; if more keys are needed, the system will automatically update
"""

import sys
import redis
from api.topics import all_tags as at





r = redis.Redis(host='0.0.0.0', port=6389, db=12)


# Each topic (tag) can have subtags of its own, as well as a count of jobs left and a count of completed jobs
for major in at.tags.keys():
    A = at.tags[major]
    B = {}
    for minor in A:
        B[minor] = {}
        B[minor]["Jobs Completed"] = []
        B[minor]["Jobs Available"] = []

    B["Jobs Completed"] = []
    B["Jobs Available"] = []

    r.hmset(major, B)
