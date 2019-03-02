"""
BASICS

Moves the output directories for each time step (given as a number) 
"""

import os, shutil



PATH = "/data/"

# Finds those directories with p, U, or T files inside
data_dirs = ['/data/'+x for x in list(os.walk(PATH))[0][1]]


# If any of them has files p, U, or T: move the entire directory

for possible_out in data_dirs:

        contents = list(os.listdir(possible_out))

        if any(var in contents for var in ['U', 'p', 'T']):
            shutil.move(possible_out, "/root/shared/results/")
