#!/usr/bin/env python3

"""
BASICS

Creates organization wide tokens, to be used when organization users apply for a token
"""


import redis
import json
import random



r = redis.Redis(host = '0.0.0.0', port = 6389, db = 3)

# Each organization requires the following data
# Name: Name of the organization, same as the key by default
# No. Users: Total number of users
# Data Plans: Max number of GB allowed per user
# Allowed users: Maximum number of authorized users from this address
# Token: Actual token
# Users: A dictionary with all the current users {Name, Last name, Email}
# Email_Term: All the allowed email terminations

Org_Name = str(input("Organization name: "))
Data_Plan = str(input("Max. allowed storage for each user: "))
if float(Data_Plan) < 0:
	print("Invalid, users cannot have negative allocations")
	raise SyntaxError

Allowed_Users = str(input("Max. number of users allowed for this organization: "))
print("Enter the list of allowed file email endings (including the @), comma separated")
Email_Term = str(input("Email ending: "))
Email_Term = ';'.join(Email_Term.replace(' ', '').split(", "))

# All tokens are 24 characters long
SEQ = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
orgtok = ''
for qq in range(0, 24):
    orgtok += random.choice(SEQ)


ORG_DATA = {'Name':Org_Name, 'No. Users':'0', 'Data Plan':Data_Plan, 'Allowed Users':Allowed_Users,
           'Organization Token':orgtok, 'Users':{}, 'Allowed Email':Email_Term}


print("New organization created: "+str(Org_Name))
print("Token: "+str(orgtok))
r.hmset(Org_Name, ORG_DATA)
