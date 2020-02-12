"""
BASICS

Set of functions to tag an image
"""


import mysql_interactions as mints



# Executes all the needed actions in a simple function that can be imported
# All variables must be string or None
def complete_tag_work(username, token, tags_provided, Image, Command, boinc_application, origin):

    # Adds job to database
    mints.add_tag(username, token, tags_provided, Image, Command, boinc_application, origin)
