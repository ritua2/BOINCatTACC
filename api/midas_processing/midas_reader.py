"""
BASICS

Analyzes the MIDAS README and draws conclusions.
Deals with finding the OS and the languages used
"""

# Finds the corresponding image to the OS
OS_chart = {'Ubuntu_16.04':'carlosred/ubuntu-midas:16.04'}
Allowed_languages = ['python', 'python3', 'go', 'c', 'c++', 'haskell', 'rust']

# Finds the OS
# 