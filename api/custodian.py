"""
BASICS

Set of functions to tag an image and mark topics
"""

import redis
import json
import topics.all_tags as at



r = redis.Redis(host='0.0.0.0', port=6389, db=12)
# Reserved words and the error message
reserved_words = ["Jobs Completed", "Jobs Available", "Images"]



# Transcribes Redis json into a dictionary
def red2dict(redin):
    return json.loads(redin.decode("UTF-8").replace('\"', 'UHJKNM').replace('\'', '\"').replace('UHJKLM', '\''))


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


# Returns the list of subtopics for a topic
def subtopics_used(topic):
    try:
        return json.loads(r.lindex("Subtopics", topic_position(topic)).decode("UTF-8"))["Subtopics"]
    except:
        raise SyntaxError('INVALID, '+str(topic)+" has never been used")


# Gets all the data for one subtopic
def subtopic_data(topic, subtopic):
    if topic not in topics_used():
        raise SyntaxError('INVALID, '+str(topic)+" has never been used")
    try:
        return red2dict(r.hget(topic, subtopic))
    except:
        raise SyntaxError('INVALID, '+str(subtopic)+" has never been used")


# Gets the topic position in a Redis list
def topic_position(topic):
    try:
        return topics_used().index(topic)
    except:
        raise SyntaxError('INVALID, '+str(topic)+" has never been used")


# Gets the image position in a Redis list
def image_position(imag):
    try:
        return images_used().index(imag)
    except:
        raise SyntaxError('Image, '+str(topic)+" has never been used")

# Adds an image to the Redis list only, not to the subtopics



# Gets the list of images for one topic
def topic_images(topic):
    try:
        A = red2dict(r.hget(topic, "Images"))
        return list(filter(None, [w.replace('\'', '') for w in A]))
    except:
        raise SyntaxError('INVALID, '+str(topic)+" has never been used")


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
def image_tags(Image):
    all_ims = images_used()
    # There will be an error if the Image is not TACC, must be accounted by the API
    A = all_ims.index(Image)
    return json.loads(r.lindex('Image Data', A).decode("UTF-8"))


# Checks the depth of a dict
def depth(d, level =0):
    if (not isinstance(d, dict)) or (not d):
        return level
    return max(depth(d[k], level + 1) for k in d)


# Adds a new Image with its corresponding topics
# Updates the topics list if needed
# TACC Images must be specified and should be done rarely
# Topics (dict/json) with topics:[subtopics], maximum of one subtopic level
# | ie:
# | {Linguistics:[syntaxis, NLP]}
def add_new_image(Image, Topics, TACC="N"):

    if not isinstance(Topics, dict):
        return 'INVALID, Only 1 subtopic is allowed per level'

    if depth(Topics) > 1:
        return 'INVALID, Only 1 subtopic is allowed per level'

    # Checks that the image either does not exist or contains a new topic
    if Image in images_used():
        IMDAT = image_tags(Image)
        IMDAT.pop('TACC')
        if IMDAT == Topics:
            return "Image is already present"
        new_image = False # Only updates some values
        pos_image = image_position(Image)
    else:
        new_image = True
        IMDAT = Topics
    
    IMDAT["TACC"] = TACC

    # Gets the topics
    if depth(d) > 1:
        raise SyntaxError('INVALID, subtopics cannot have subtopics')

    all_topics = topics_used()

    for jk in Topics.keys():
        JK = jk.upper()
        # Avoids errors if the same subtopic is written twice
        subs = list(set(Topics[jk]))
        # Gets images

        # Keeps reserved words from appearing as subtopics
        if any(resword in subs for resword in reserved_words):
            return 'INVALID, \''+'\' \''.join(reserved_words)+'\' are reserved words, cannot be subtopics'

        # Checks if the image is already accounted for
        # Image is automatically added to a subtopic when created
        TIM = topic_images(JK)
        if Image in TIM:
            continue

        if JK in all_topics:
            # Checks the subtopics, updates if needed
            pos_topic = topic_position(JK)
            basic_sub = json.loads(r.lindex("Subtopics", pos_topic).decode("UTF-8"))
            all_subs = basic_sub["Subtopics"]

            for stt in subs:
                STT = stt.upper()
                if STT in all_subs:
                    # Checks if the image exists
                    subdata = subtopic_data(JK, STT)
                    if Image in subdata:
                        continue
                    # Adds image and updates
                    # Gets the data and appends the image to it
                    subdata["Images"].append(Image)
                    # Also adds the image to the main system
                    TIM.append(Image)
                    r.hset(JK, STT, subdata)
                    basic_sub["Subtopics"].append(STT)
                    continue

                # Creates a new subtopic
                Minor = {"Jobs Completed":[], "Jobs Available":[], "Images":[Image]}
                TIM.append(Image)
                r.hset(JK, STT, Minor)
                basic_sub["Subtopics"].append(STT)

            # Corrects the list of images and subtopics total
            r.lset("Subtopics", pos_topic, json.dumps(basic_sub))
            r.hset(JK, "Images", TIM)

        # Creates a new topic
        NewTOP = {"Images":[Image], "Jobs Completed":[], "Jobs Available":[]}
        asub = [] #Subtopics
        for stt in subs:
            STT = stt.upper()
            NewTOP[STT] = {"Images":[Image], "Jobs Completed":[], "Jobs Available":[]}
            asub.add(STT)
        r.hmset(JK, NewTOP)
        r.rpush('Topics', JK)
        r.rpush('Subtopics', json.dumps({'Subtopics':asub}))


    # Finally, adds the image to the list with its corresponding data
    # If the image already exists, it simply updates the information
    if new_image:
        r.rpush('Known Images', Image)
        r.rpush('Image Data', json.dumps(IMDAT))
        return "Added new image"

    # Adds new topics to existing images
    # Checks every topic one by one
    curtops = IMDAT.keys()
    for Top in Topics.keys():
        if Top in curtops:
            for Sub in Topics[Top]:
                if Sub not in IMDAT[Top]:
                    IMDAT[Top].append(Sub)
                # Do nothing if subtopic already present

        # Create new topic maintaining the subtopics
        IMDAT[Top] = Topics[Top]

    r.lset('Image Data', pos_image, json.dumps(IMDAT)) 
    return "Updated Image with new topics"


# Adds a new topic and subtopics
# subtops (arr) (str): List of subtopics
def add_new_topic(topic, subtops):
    if topic in topics_used():
        # Checks the subtopics
        cursubs = subtopics_used(topic)
        if all(sub in cursubs for sub in subtops):
            return "Topic already exists"
        # Adds a new subtopic

    # Adds a new topic


