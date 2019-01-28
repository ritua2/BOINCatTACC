"""
BASICS

Submitting data to redis in a Noob way.
No need to check some stuff, we can assume the whole database works linearly.
"""

import glob, os
import redis
import datetime

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
# linlin (str): Line in the file
def summarizer(linlin):
   
   LLL = linlin.split(' ')
   # The docker image should always be the first thing
   L1 = LLL[0]
   L2 = ' '.join(LLL[1::])
   return [L1, L2]



for file in glob.glob("/home/boincadm/project/html/user/token_data/process_files/*.txt"):
    
    with open(file, "r") as filproc:    
         # Moves all the data into redis   
         for line in filproc:
             BB = line.replace('\n', '')
             # Skips the token line
             if len(BB.split(' ')) == 1:
                continue
             summar = summarizer(BB)
             # Redis has the following columns:
             # Token, Image (Dockerhub), Command, Date submitted
             # Date run (set to 0 now, job not run run yet)
             # All time stamps are YYYY-MM-DD HH:MM:SS in local time
             prestime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
             r.rpush('Token', get_token(file))
             r.rpush('Image', summar[0])
             r.rpush('Command', summar [1])
             r.rpush('Date (Sub)', prestime)
             r.rpush('Date (Run)', '0')
             r.rpush('Error', '0')
             r.rpush('Notified', '0')

 
    # Erases the file
    os.remove(file)
