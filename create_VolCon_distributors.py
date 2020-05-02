"""
BASICS

Sets the VolCon parameters for the corresponding mirrors
This program must only be run once; VolCon systems will automatically connect with the corresponding API in order to update themselves

Rerun this program to restart (will erase all current mirrors)
"""



import hashlib
import redis
import random
import sys


r = redis.Redis(host = '0.0.0.0', port = 6389, db = 3)




# Deletes information about all current VolCon mirrors if they are already set-up
if r.hexists("VolCon", 'Organization Token'):
    answer = str(input("VolCon mirrors are already setup, y to delete them (this action is not recoverable): "))

    if answer == "y":
        K = [H.decode("UTF-8") for H in r.hkeys("VolCon")]
        H = [h for h in K if "M-"==h[:2]]
        for mirror in H:
            r.delete(mirror)
        r.delete("VolCon")
        print("Mirrors have been deleted, rerun this program to set up information about new ones")
        print("You will need to set the connections again in each possible new mirror")
        sys.exit()

    else:
        print("Mirrors were not erased")
        sys.exit()



# A password is required in order to join as a mirror
password = hashlib.sha256(input("Enter VolCon password: ").encode('UTF-8')).hexdigest()
Org_Name = "VolCon"


# For future records, all mirrors must start with M-{MIRROR IP} and will be provided as keys inside this hash
# They will also appear as individual hashes inside Redis(db=3)

VolCon = {'Name':Org_Name, 'Organization Token':password, 'Available-Mirrors':'0', "Type":"VolCon"}


r.hmset("VolCon", VolCon)


