"""
BASICS

Finds all the output files, moves them to /root/shared/results if not there by default
"""

import os, shutil
from glob import glob


PATH = "/data/"

Gib_outs = [PATH+x for x in os.listdir(PATH)]

# For some reason, these are not accounted for in the find command
# Add them to the end file

# Ignores files starting with a dot, or without it at all
Predots = [line.rstrip('\n') for line in open('/All_outs.txt') for y in glob(os.path.join(x[0], '*.*'))]

for exot in Gib_outs:

	AAA = False # Keeps track if a particular file has already been seen

		# Must be different to all checked
        for alin in Predots:
                if exot == alin:
                    AAA = True
                    break

        
        # Only moves those unaccounted
        if AAA==False:
        	shutil.move(exot, "/root/shared/results/"+exot.split('/')[-1]) 
