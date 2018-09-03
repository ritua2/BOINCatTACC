"""
BASICS

Set of functions to tag an image and mark topics
"""

import redis
import json
import topics.all_tags as at



r = redis.Redis(host='0.0.0.0', port=6389, db=12)



# Returns the number of images used
def nim_used():
    return r.llen("Known Images")


# Returns the list of current images used
def images_used():
    return [r.lindex("Known Images", x).decode("UTF-8") for x in range(0, nim_used())]


# Returns the number of topics used
def ntopics_used():
    return r.llen('Topics')


# Returns the list of topics used
def topics_used():
    return [r.lindex("Topics", x).decode("UTF-8") for x in range(0, ntopics_used())]


# Returns the list of all TACC images
def TACC_images_used():
    all_ims = images_used()
    # Gets the json information
    jinfo = [json.loads(r.lindex('Image Data', y).decode("UTF-8")) for y in range(0, len(all_ims))]
    return [y for y, z in zip(all_ims, jinfo) if (z['TACC'] == 'Y')]
    

# Checks if an Image is provided by TACC
def image_is_TACC(Image):
    if Image in TACC_images_used():
        return True

    return False


# Gets the tags associated with an image
def taccim_tags(Image):

    all_ims = images_used()
    # There will be an error if the Image is not TACC, must be accounted by the API
    A = all_ims.index(Image)
    return json.loads(r.lindex('Image Data', A).decode("UTF-8"))


# Checks the depth of a dict
def depth(d):
    level = 0
    if not isinstance(d, dict) or not d:
        raise SyntaxError('INVALID, data structure is not dict')
    return max(depth(d[k], level + 1) for k in d)


# Adds a new Image with its corresponding topics TODO TODO TODO TODO TODO TODO
# TACC Images must be specified and should be done rarely
# Topics (dict/json) with topics, maximum of one subtopic
def add_new_image(Image, Topics, TACC=False):

    if depth(Topics) > 1:
        raise SyntaxError('Only 1 subtopic is allowed per level')

    if Image in images_used():
        return "Image is already present"

    # Gets the topics






    r.rpush("Known Images", Image)


# Adds a new topic to an existing image
