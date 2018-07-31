"""
BASICS

Generates a token for any user provided their name
"""

import os, sys
import random
import redis
import requests


r = redis.Redis(host = '0.0.0.0', port = 6389, db =2)


# Checks if there are enough arguments


if len(sys.argv) < 4:
   print("Not enough arguments. Provide the following (space  separated):\n {FIRSTNAME} {LASTNAME} {EMAIL} {ALLOCATION (GB) (Optional)}")
   print("If no allocation is provided, then 2 GB will be assigned")
   sys.exit(1)

if len(sys.argv) > 5:
   print("Too many arguments. Provide the following (space separated):\n {FIRSTNAME} {LASTNAME} {EMAIL} {ALLOCATION (GB) (Optional)}")
   print("If no allocation is provided, then 2 GB will be assigned")
   sys.exit(1)


with open("Tokens.txt", "a") as tokfile:
    

     # All tokens are 14 characters long
     SEQ = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
     rantok = ''
     for qq in range(0, 14):
         rantok += random.choice(SEQ)

     tokfile.write(sys.argv[1]+" "+sys.argv[2]+", "+rantok+", "+sys.argv[3]+"\n")
     
     # Creates the user allocation 
     if len(sys.argv) == 4:
        r.set(rantok, '2')
        print("User allocation has been set to 2 GB")
     else:
        r.set(rantok, float(sys.argv[4]))
        print("User allocation has been set to "+str(sys.argv[4])+" GB")

     # Creates a Reef set-up on the external Reef server
     requests.get('http://'+os.environ['Reef_IP']+':2002/reef/create_user/'+rantok+'/'+os.environ['Reef_Key'])     


print("New assigned token is: "+str(rantok))
