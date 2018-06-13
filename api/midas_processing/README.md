### MIDAS guide

**Set-up**
MIDAS (Multiple Input Docker Automation System) is a TACC tool designed for automatic dockerization. To use this tool, use the MIDAS API to submit either a *.tgz* or a *tar.gz* file containing all the necessary files.  
All files to be used must be inside, as well as a README.txt (required name, files without it will return an error) containing the set-up information.
To do so, use:
 ```bash
 	curl -F midas_file=MY_COMPRESSED_FILE.tgz http://SERVER_IP:5085/v2/midas_job/token=TOKEN
 ```

#### README.txt 

Required for MIDAS processing, it has 5 required sections (OS, LANGUAGE, LIBRARY, COMMAND, OUTPUT) and an optional one (USER_SETUP).  
The absence of any of the required sections will raise an error, and keep the user from continuing.  
Lines starting with *H* are comments. Same-line comments are not allowed.  The use of any OS or language not supported requires the user to create a set-up file.  Users are responsible to make sure that their programs run succesfully with files only allowed in local directories.  
For examples for README.txt, 3 will be provided in this same directory: python, C++, setup file.

**OS**
Refers to the base OS on which all the other commands are run. 
Introduced by:
*OS)*  
The following OS are supported, and they are written as:
Ubuntu 16.04
```
	OS) Ubuntu_16.04
```
