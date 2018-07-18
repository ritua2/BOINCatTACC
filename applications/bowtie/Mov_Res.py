"""
BASICS

Finds all the output files, moves them to /root/shared/results if not there by default
Does not move binary files, act accordingly
"""

import os, shutil
from glob import glob
from binaryornot.check import is_binary


PATH = "/data/"

Gib_outs = [PATH+x for x in os.listdir(PATH)]

# For some reason, these are not accounetd for in the find command
# Add them to the end file


for exot in Gib_outs:


    # Skips binary files
    if is_binary(exot):
        continue

        
    # Only moves those unaccounted
    shutil.move(exot, "/root/shared/results/"+exot.split('/')[-1]) 
