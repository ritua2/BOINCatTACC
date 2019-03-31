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


new_cluster = str(input("Enter cluster name: "))

if (new_cluster == "ORGS") or (new_cluster == "VolCon"):
    print("Name '"+new_cluster+"' is already used for internal purposes")
    sys.exit()


# Deletes information about all current VolCon mirrors if they are already set-up
if r.exists(new_cluster):

    if r.hexists("ORGS", new_cluster):
        print("Name '"+new_cluster+"' is already an organization")
        sys.exit()


    answer = str(input("'"+new_cluster+"' cluster is already setup, y to delete it (this action is not recoverable): "))

    if answer == "y":
        K = [H.decode("UTF-8") for H in r.hkeys(new_cluster)]
        H = [h for h in K if new_cluster in h]
        for runner in H:
            r.delete(runner)
        r.delete(new_cluster)
        print(new_cluster+" cluster and its constituent runners have been deleted from the system, rerun this program to set up new ones")
        sys.exit()

    else:
        print("Cluster was not erased")
        sys.exit()


# A password is required in order to join as a mirror
password = hashlib.sha256(input("Enter cluster password: ").encode('UTF-8')).hexdigest()

while True:

    GPU_yn = str(input("Will the cluster accept GPU jobs [y/n]? "))
    if (GPU_yn != "y") and (GPU_yn != "n"):
        print("Invalid answer")
        continue

    if GPU_yn == "y":
        GPU_yn = 1
    else:
        GPU_yn = 0

    break


# For future records, all cluster elements must start with cluster-{MIRROR IP} and will be provided as keys inside this hash
# They will also appear as individual hashes inside Redis(db=3)

cluster_info = {'Name':new_cluster, 'Organization Token':password, "Type":"VolCon-client", "GPU":GPU_yn}

r.hmset(new_cluster, cluster_info)

