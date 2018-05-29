"""
BASICS

Ensures that all columns in the Redis database have the same rows.
If not, it invalidates the whole row.
Saves the data at the end.
"""

import redis
import shutil


r = redis.Redis(host ='0.0.0.0', port = 6389, db =0)
cols = ['Token', 'Image', 'Command', 'Date (Sub)', 'Date (Run)', 'Error', 'Notified']

if len(list(set([r.llen(x) for x in cols]))) == 1:
   print('Nothing to see, program works fine')

else:

   # The entire row is invalidated
   appropriate_rows = max([r.llen(y) for y in cols])
   first_error = min([r.llen(y) for y in cols])
   for title in cols:
       for hh in range(r.llen(title), appropriate_rows):
           r.rpush(title, 'Incorrect order, row deleted')
       for nvnv in range(first_error, appropriate_rows):
           r.lset(title, nvnv, 'Incorrect order, row deleted')
