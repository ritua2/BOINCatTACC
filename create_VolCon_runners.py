"""
BASICS

Creates a VolCon organization (more than one can exist at any time)
This program must only be run once; VolCon systems will automatically connect with the corresponding API in order to update themselves

Rerun this program with the name of a known ORG to restart it
"""



import hashlib
import redis
import random
import sys


r = redis.Redis(host = '0.0.0.0', port = 6389, db = 3)


new_org = str(input("Enter cluster name: "))

if (new_org == "ORGS") or (new_org == "VolCon"):
    print("Name '"+new_org"' is already used for internal purposes")
    sys.exit()


# Deletes information about all current VolCon mirrors if they are already set-up
if r.hexists(new_org, 'Organization Token'):
    answer = str(input("'"+new_org+"' cluster is already setup, y to delete it (this action is not recoverable): "))

    if answer == "y":
        K = [H.decode("UTF-8") for H in r.hkeys(new_org)]
        H = [h for h in K if new_org in h]
        for runner in H:
            r.delete(runner)
        r.delete(new_org)
        print(new_org+" cluster and its constituent runners have been deleted from the system, rerun this program to set up new ones")
        sys.exit()

    else:
        print("Cluster was not erased")
        sys.exit()


# A password is required in order to join as a mirror
password = hashlib.sha256(input("Enter cluster password: ").encode('UTF-8')).hexdigest()


# For future records, all mirrors must start with M-{MIRROR IP} and will be provided as keys inside this hash
# They will also appear as individual hashes inside Redis(db=3)

org_info = {'Name':new_org, 'Organization Token':password, 'Available-Mirrors':'0', "Type":"VolCon"}


r.hmset(new_org, org_info)


