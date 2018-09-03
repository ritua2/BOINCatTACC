"""
BASICS

Set of functions to tag an image and mark topics
"""

import redis
import json
import all_tags as at



r = redis.Redis(host='0.0.0.0', port=6389, db=12)



# Returns the number of images used
def nim_used():
    return r.llen("Known Images")


# Returns the list of current images used
def images_used():
    return [r.lindex("Known Images", x).decode("UTF-8") for x in range(0, nim_used())]


# Returns the list of all TACC images
def TACC_images_used():
    all_ims = images_used()
    # Gets the json information
    jinfo = [json.loads(r.lindex('Image Data', y).decode("UTF-8")) for y in range(0, len(all_ims))]
    return [y for y, z in zip(all_ims, jinfo) if (z['TACC'] == 'Y')]
    

# Gets the tags associated with an image
def taccim_tags(Image):

    all_ims = images_used()
    # There will be an error if the Image is not TACC, must be accounted by the API
    A = all_ims.index(Image)
    return json.loads(r.lindex('Image Data', A).decode("UTF-8"))
