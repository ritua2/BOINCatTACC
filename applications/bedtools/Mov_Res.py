"""
BASICS

Finds all the output files, moves them to /root/shared/results if not there by default
"""

import os, shutil
from glob import glob


PATH = "/data"

# Adds all the text and image formats (only JPG, JPEG, PNG are accepted)
Gib_outs = [y for x in os.walk(PATH) for y in glob(os.path.join(x[0], '*.txt'))]
Gib_outs += [y for x in os.walk(PATH) for y in glob(os.path.join(x[0], '*.jpg'))]
Gib_outs += [y for x in os.walk(PATH) for y in glob(os.path.join(x[0], '*.jpeg'))]
Gib_outs += [y for x in os.walk(PATH) for y in glob(os.path.join(x[0], '*.png'))]

# For some reason, these are not accounetd for in the find command
# Add them to the end file
#Unaccounted_accounted = [accx.txt,  accy.txt,  backbone.txt,  dispx.txt,  dispy.txt,  example3.txt,  example4.txt,  pwp.txt,  strain9.txt,  stress9.txt]

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
