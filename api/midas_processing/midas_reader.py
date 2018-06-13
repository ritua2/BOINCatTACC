"""
BASICS

Analyzes the MIDAS README and draws conclusions.
Deals with finding the OS and the languages used
"""

# Finds the corresponding image to the OS
OS_chart = {'Ubuntu_16.04':'carlosred/ubuntu-midas:16.04'}
Allowed_languages = ['python', 'python3', 'go', 'c', 'c++', 'haskell', 'rust']




# Verifies that a file has all 5 required inputs
# README_path (str): Must be the full path to the README
def valid_README(README_path):
	
    qualifier = [['OS)', 'LANGUAGE)', 'COMMAND)', 'OUTPUT)'], [0, 0, 0, 0]]

    for nvnv in range(0, len(qualifier[0])):
        with open(README_path, 'r') as README:
            for line in README:
                if qualifier[0][nvnv] in line:
                    qualifier[1][nvnv] = 1
                    break

    if 0 in qualifier[1]:
        return False
    return True


# Finds the OS
def valid_OS(README_path):

    with open(README_path, "r") as README:
        for line in README:
            # Only one OS is needed
            for onos in OS_chart.keys():
                if onos in line:
                    return onos
        
    # OS must be specified
    raise
