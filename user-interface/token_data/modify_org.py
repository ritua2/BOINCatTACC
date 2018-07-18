#!/usr/bin/env python3

"""
BASICS

Modifies an organization's creadentials or acquires information about it
Also allows to check organization user information
"""


import redis
import json
import random
import sys



r = redis.Redis(host = '0.0.0.0', port = 6389, db = 3)

if len(sys.argv) == 1:
    print("No arguments provided, use -h or --help for help")
    print("\nInformation:")
    print('Modifies an organization credentials, erases organizations, or checks the user information')
    print('Use the following flags to set up the following action:')
    print('  -all: Returns a list of names and information of all the organizations')
    print('  -names: Returns a list of names of all organizations')
    print('  -token ORG_NAME: Returns an org token')
    print('  -org_info ORG_NAME: Returns all the information about the organnization')
    print('  -users ORG_NAME: Returns information about all the users in an organization')
    print('  -delete ORG_NAME: Deletes an organization')
    sys.exit()


command = sys.argv[1]
all_orgs = r.keys()

if command == '-all':
   for y in all_orgs:
       print(r.hgetall(y.decode('UTF-8')))
   sys.exit()


if command == '-names':
   print('Available organizations:')
   for y in all_orgs:
       print(y.decode('UTF-8'))
   sys.exit()

if command == '-token':
   try:
      ORG_NAME = sys.argv[2]
      # Decodes the entire dictionary
      deco = {k.decode('utf8'): v.decode('utf8') for k, v in r.hgetall(ORG_NAME).items()}
      print(deco['Organization Token'])

   except:
      print("Organization does not exist")
   sys.exit()

if command == '-org_info':
   try:
      ORG_NAME = sys.argv[2]
      # Decodes the entire dictionary
      deco = {k.decode('utf8'): v.decode('utf8') for k, v in r.hgetall(ORG_NAME).items()}
      print(deco)
   except:
      print("Organization does not exist")
   sys.exit()

if command == '-users':
   try:
      ORG_NAME = sys.argv[2]
      # Decodes the entire dictionary
      deco = {k.decode('utf8'): v.decode('utf8') for k, v in r.hgetall(ORG_NAME).items()}
      print(deco['Users'])
   except:
      print("Organization does not exist")
   sys.exit()

if command == '-delete':
   try:
      ORG_NAME = sys.argv[2]
      # Decodes the entire dictionary
      r.delete(ORG_NAME)
      print('Organization deleted, all its data has been erased')
   except:
      print("Organization does not exist")
   sys.exit()
