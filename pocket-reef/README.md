### Portable, transferrable cloud storage

Pocket-Reef (PR) is an extension of the Reef stoorage system within the main BOINC server.  
It will store regular files and results without changes and returning them on demand.  
All your files will remain protected and visible only to you. This new system also has the advantage of reducing the disk requirements
for the main BOINC server, allowing researchers to submit more jobs while reducing the server requirements.



#### Installation

Pocket Reef is designed as a complement to a BOINC server, although it can also be used to store personal data.  


**Instructions**  
* Clone this current directory
* Chnage directory
* (RECOMMENDED) Change the Reef key in the dockerfile
* Build the docker image and log into it in a detached mode

```bash
	git clone https://github.com/ritua2/TACC-2-BOINC/tree/master/pocket-reef
	cd pocket-reef
	# Change the Reef key (recommended)
	vi Dockerfile
	Docker build -t $REEF_IMAGE_NAME .
```
