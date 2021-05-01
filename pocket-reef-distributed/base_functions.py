"""
BASICS

Contains a set of functions that are called accross the other APIs
"""

import os
import mysql.connector as mysql_con

REEF_FOLDER="/rdat/sandbox"

# Returns the list of elements of l1 not in l2
# l1 (arr) (generic)
# l2 (arr) (generic)
# returns (arr)
def l2_contains_l1(l1, l2):
    return[elem for elem in l1 if elem not in l2]

# separator (str)
def error__l2_contains_l1(l1, l2, separator=","):
    check = l2_contains_l1(l1, l2)

    if check:
        return [True, separator.join([str(a) for a in check])]
    else:
        return [False, ""]

# Checks if the provided user key is valid
def valid_key(ukey):

    if ukey == os.environ['Reef_Key']:
        return True
    return False

# Checks if the user is valid
def valid_user(unam):
    grey_db = mysql_con.connect(host = os.environ["URL_BASE"] , port = 6602, user = os.environ["MYSQL_USER"] , password = os.environ["MYSQL_PASSWORD"], database = os.environ["MYSQL_DATABASE"])
    cursor = grey_db.cursor(buffered=True)
    cursor.execute("select * from user where name=%s",(unam,))
    uc=None
    for row in cursor:
        uc=row[0]
    cursor.close()
    grey_db.close()
    if uc != None:
        return True
    else:
        return False

# Get available VM with required space
def get_available_vms(size):
    grey_db = mysql_con.connect(host = os.environ["URL_BASE"] , port = 6602, user = os.environ["MYSQL_USER"] , password = os.environ["MYSQL_PASSWORD"], database = os.environ["MYSQL_DATABASE"])
    cursor = grey_db.cursor(buffered=True)
    cursor.execute("select ip, node_key from node where status='Available' and free_space > %s order by free_space",(size,))
    ip=[]
    nkey=[]
    for row in cursor:
        ip.append(row[0])
        nkey.append(row[1])
    cursor.close()
    grey_db.close()
    return ip,nkey

# get VM containing the file 
def get_file_vm(userid,file,dir):
    grey_db = mysql_con.connect(host = os.environ["URL_BASE"] , port = 6602, user = os.environ["MYSQL_USER"] , password = os.environ["MYSQL_PASSWORD"], database = os.environ["MYSQL_DATABASE"])
    cursor = grey_db.cursor(buffered=True)
    cursor.execute("select ip from file where user_id=%s and id=%s and directory=%s",(userid,file,dir))
    ip=None
    nkey=None
    for row in cursor:
        ip=row[0]
    if ip is not None:
        cursor.execute("select node_key from node where ip=%s",(ip,))
        for row in cursor:
            nkey=row[0]
    cursor.close()
    grey_db.close()
    return ip,nkey


# return size of the directory in bytes
def get_dir_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

# add directory details to database if it's not there
def add_dir(ip,userid,dir):
    grey_db = mysql_con.connect(host = os.environ["URL_BASE"] , port = 6602, user = os.environ["MYSQL_USER"] , password = os.environ["MYSQL_PASSWORD"], database = os.environ["MYSQL_DATABASE"])
    cursor = grey_db.cursor(buffered=True)
    cursor.execute("insert ignore into file set ip=%s, user_id=%s, directory=%s, id='', is_dir=TRUE",(ip,userid,dir))
    grey_db.commit();
    cursor.close()
    grey_db.close()

# add file details to database if it's not there
def add_file(ip,userid,dir,file):
    grey_db = mysql_con.connect(host = os.environ["URL_BASE"] , port = 6602, user = os.environ["MYSQL_USER"] , password = os.environ["MYSQL_PASSWORD"], database = os.environ["MYSQL_DATABASE"])
    cursor = grey_db.cursor(buffered=True)
    cursor.execute("insert ignore into file set ip=%s, user_id=%s, directory=%s, id=%s, is_dir=FALSE",(ip,userid,dir,file))
    grey_db.commit();
    cursor.close()
    grey_db.close()

# remove file from the database
def remove_file(ip,userid,dir,file):
    grey_db = mysql_con.connect(host = os.environ["URL_BASE"] , port = 6602, user = os.environ["MYSQL_USER"] , password = os.environ["MYSQL_PASSWORD"], database = os.environ["MYSQL_DATABASE"])
    cursor = grey_db.cursor(buffered=True)
    cursor.execute("delete from file where ip=%s and user_id=%s and id=%s and directory=%s and is_dir=FALSE",(ip,userid,file,dir))
    grey_db.commit()
    cursor.close()
    grey_db.close()

# remove each directory and sub-directories
def remove_dir(ip,userid,directory):
    grey_db = mysql_con.connect(host = os.environ["URL_BASE"] , port = 6602, user = os.environ["MYSQL_USER"] , password = os.environ["MYSQL_PASSWORD"], database = os.environ["MYSQL_DATABASE"])
    cursor = grey_db.cursor(buffered=True)
    cursor.execute("delete from file where ip=%s and user_id=%s and directory like %s",(ip,userid,directory+"%"))
    grey_db.commit()
    cursor.close()
    grey_db.close()

# update free space
def update_node_space(ip):
    grey_db = mysql_con.connect(host = os.environ["URL_BASE"] , port = 6602, user = os.environ["MYSQL_USER"] , password = os.environ["MYSQL_PASSWORD"], database = os.environ["MYSQL_DATABASE"])
    cursor = grey_db.cursor(buffered=True)
    cursor.execute("select total_space from node where ip=%s",(ip,))
    totalspace=None
    for row in cursor:
        totalspace=row[0]
    occupiedspace=get_dir_size(REEF_FOLDER)
    if (totalspace-occupiedspace) > 0:
        cursor.execute("update node set free_space=%s, status='Available' where ip=%s",((totalspace-occupiedspace),ip))
    else:
        cursor.execute("update node set free_space=%s, status='Full' where ip=%s",((totalspace-occupiedspace),ip))
    grey_db.commit()
    cursor.close()
    grey_db.close()

# Returns a dictionary showing all the files in a directory (defaults to working directory)
def get_user_files(userid,DIR=''):
    files={}
    grey_db = mysql_con.connect(host = os.environ["URL_BASE"] , port = 6602, user = os.environ["MYSQL_USER"] , password = os.environ["MYSQL_PASSWORD"], database = os.environ["MYSQL_DATABASE"])
    cursor = grey_db.cursor(buffered=True)
    cursor.execute("select id,user_id from file where user_id=%s and directory=%s",(userid,DIR))
    file=[]
    usr=None
    #dir=[]
    for row in cursor:
        usr=row[1]
        if row[0]=='':
            continue
        file.append(row[0])
    cursor.close()
    grey_db.close()
    return file,usr
