"""
BASICS

Set of functions to tag an image and mark topics
"""

import redis
import all_tags as at



r = redis.Redis(host='0.0.0.0', port=6389, db=12)



# Returns the number of images used
def nim_used():
	return r.llen("Known Images")


# Returns the list of current images used
def images_used():
	return [r.lindex("Known Images", x).decode("UTF-8") for x in range(0, nim_used())]


# Gets the tags associated with a TACC image
def taccim_tags(Image):

	try:
		return at.TACCIM["Image"]
	except:
		raise SyntaxError("INVALID, Image is not provided by TACC")
