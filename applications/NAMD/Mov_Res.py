"""
BASICS

Finds all the output files, moves them to /root/shared/results if not there by default and change stheir type to text files
"""

import os, shutil
from glob import glob


PATH = "/data"

Gib_outs = [y for x in os.walk(PATH)]

# For some reason, these are not accounetd for in the find command
# Add them to the end file

Predots = [line.rstrip('\n') for line in open('/All_outs.txt')]

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
