import sys


with open("test.txt", "w") as ff:
     ff.write("Test: "+str(sys.argv[1]))




