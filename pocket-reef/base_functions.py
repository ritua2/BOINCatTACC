"""
BASICS

Contains a set of functions that are called accross the other APIs
"""

import os



# Checks if the provided user key is valid
def valid_key(ukey):

    if ukey == os.environ['Reef_Key']:
        return True
    return False
