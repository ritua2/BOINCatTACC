"""
BASICS

Submitting data to redis in a Noob way.
No need to check some stuff, we can assume the whole database works linearly.
"""

import glob, os
import redis


r = redis.Redis(host = '0.0.0.0', port = 6389, db =0)


# Finds the token in a particular file, always in the last line of the file
# afil (str): Name and directory of the file

def get_token(afil):
    
    with open(afil, 'r') as rrf:
        
        for line in rrf:
            # The token is the only line that does not have any spaces in it
            AA = line.replace('\n', '').split(' ')
            if (len(AA) == 1) and (AA != ['']):
               return AA[0]


# Returns the commands in a text file to submit the result to redis   
# The result is an array of the form:
# ['{Image in D-Hub}', '{COMMAND}']



for file in glob.glob("./process_files/*.txt"):
    print(file)
    print(get_token(file))
    
    # Moves all the data into redis   
