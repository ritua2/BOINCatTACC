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
Gib_outs += [y for x in os.walk(PATH) for y in glob(os.path.join(x[0], '*.cfg'))]
Gib_outs += [y for x in os.walk(PATH) for y in glob(os.path.join(x[0], '*.log'))]


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
