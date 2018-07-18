"""
BASICS

Only moves specific files to the ouput directory.
If the files do not exist, it will not raise an error, it will simply not move the file.
"""

import os, shutil
from glob import glob


PATH = "/work/"

# Finds the files needed to move
mov_files = []
with open(PATH+"README.txt", "r") as README:

	for line in README:
		LLL = line.replace('\n', '')
		if '[OUTPUT]' in LLL:
			file_to_be_moved = LLL.replace('[OUTPUT]', '').replace(' ', '')
			if 'ALL' == file_to_be_moved:
				mov_files = os.listdir(PATH)
				break

			mov_files.append(file_to_be_moved)

# Actually moves the files
for afil in mov_files:
	try:
		shutil.move(afil, "/root/shared/results/"+afil) 
	except:
		pass
		