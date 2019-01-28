"""
BASICS

Runs the last submitted command

DEPRECATED
"""


import os


# Checks if a particular line is inside the file
def checker(this_line):

	with open("allrun.txt", "r") as existing:

		for line in existing:

			if this_line == line.replace("\n", ""):
				return True

	# Line is already in the file
	return False


with open("issued.txt", "r") as all_issued:

	for alin in all_issued:

		if checker(alin.replace("\n", "")) == False:

			# Adds to the file and runs it in the server

			FF2 = open("allrun.txt","a") 
			FF2.write(alin+"\n") 
			FF2.close()

			# Executes the command on the shell 
			os.system("/home/boincadm/project/bin/boinc2docker_create_work.py " + alin.replace("\n", ""))                         
			