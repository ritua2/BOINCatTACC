"""
BASICS

Sets the VolCon parameters for the corresponding mirrors
This program must only be run once; VolCon systems will automatically connect with the corresponding API in order to update themselves

Rerun this program to restart (will erase all current mirrors)
"""



import hashlib
import redis
import random



r = redis.Redis(host = '0.0.0.0', port = 6389, db = 3)


# A password is required in order to join as a mirror
password = hashlib.sha256(input("Enter VolCon password: ").encode('UTF-8')).hexdigest()
Org_Name = "VolCon"


# For future records, all mirrors must start with M-{MIRROR IP} and will be provided as keys inside this hash
# They will also appear as individual hashes inside Redis(db=3)

VolCon = {'Name':Org_Name, 'Organization Token':password, 'Available-Mirrors':'0', "Type":"VolCon"}


r.hmset("VolCon", VolCon)


