"""
BASICS

Necessary functions for API work
"""

import random

# Finds if the token is valid
def token_test(token):

   if len(token) < 14:
   	   return False

   with open("../html/user/token_data/Tokens.txt", "r") as TFIL:
       for line in TFIL:
           if token in line:
              return True
       else:
           return False

# Creates a random file name with 18 characters

def random_file_name():

    HHH = 'abcdefghijklmnopqrstuvwxyz1234567890'
    fnam = "auk"
    for qq in range(0, 12):
        fnam += random.choice(HHH)
    else:
        fnam += ".txt"
    return fnam

