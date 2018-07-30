"""
BASICS

Finds all the output files, moves them to /root/shared/results if not there by default
Does not move binary files, act accordingly
"""

import os, shutil
from glob import glob


PATH = "/data/"

Gib_outs = [PATH+x for x in os.listdir(PATH)]



# Moves all files

for exot in Gib_outs:
        
    # Only moves those unaccounted
    shutil.move(exot, "/root/shared/results/"+exot.split('/')[-1]) 
