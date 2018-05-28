"""
BASICS

Necessary functions for API work
"""

def token_test(token):

   if len(token) < 14:
   	   return False

   with open("../html/user/token_data/Tokens.txt", "r") as TFIL:
       for line in TFIL:
           if token in line:
              return True
       else:
           return False
