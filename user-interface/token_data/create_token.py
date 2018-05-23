"""
BASICS

Generates a token for any user provided their name
"""

import sys
import random


# Checks if there are enough arguments


if len(sys.argv) < 3:
   print("Not enough arguments. Provide the following (comma separated):\n {FIRSTNAME}, {LASTNAME}")
   sys.exit(1)

if len(sys.argv) > 3:
   print("Too many arguments. Provide the following (comma separated):\n {FIRSTNAME}, {LASTNAME}")
   sys.exit(1)


with open("Tokens.txt", "a") as tokfile:
    

     # All tokens are 14 characters long
     SEQ = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
     rantok = ''
     for qq in range(0, 14):
         rantok += random.choice(SEQ)

     tokfile.write(sys.argv[1]+" "+sys.argv[2]+", "+rantok+"\n")
 
print("New assigned token is: "+str(rantok))