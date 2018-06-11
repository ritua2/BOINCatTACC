"""
BASICS

Necessary functions for API work
"""

import random
import os

# Finds if the token is valid
def token_test(token):

   if len(token) < 14:
   	   return False

   with open("/root/project/html/user/token_data/Tokens.txt", "r") as TFIL:
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


# Creates a random directory name for MIDAS use
# All directories are 11 characters long

def random_dir_name():

    TTT = 'abcdefghijklmnopqrstuvwxyz1234567890'
    dirnam = 'dir-'
    for qq in range(0, 7):
        dirnam += random.choice(HHH)

    return fnam


# Computes the size of an user's sandbox
# TOK (str): Token

def user_sandbox_size(TOK):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk('/root/project/api/sandbox_files/DIR_'+TOK):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size
