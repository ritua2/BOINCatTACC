### Portable, transferrable cloud storage

Pocket-Reef (PR) is an extension of the Reef stoorage system within the main BOINC server.  
It will store regular files and results without changes and returning them on demand.  
All your files will remain protected and visible only to you. This new system also has the advantage of reducing the disk requirements
for the main BOINC server, allowing researchers to submit more jobs while reducing the server requirements.



#### Installation

Pocket Reef is designed as a complement to a BOINC server, although it can also be used to store personal data.  


**Instructions**  
* Clone this current directory
* Change directory
* Change the Reef key (recommended)
* Set up the docker compose

```bash
	git clone https://github.com/ritua2/BOINCatTACC
	cd BOINCatTACC/pocket-reef
	# Change the Reef key (recommended)
	vi docker-compose.yml
	docker-compose up -d
```

**Usage**  
To activate or switch off the APIs, enter the docker container and do:  

```bash
	# Enter container
	docker exec -it $CONTAINER bash
	cd /reef
	# Activate
	./API_Daemon.sh -up
	# Deactivate
	./API_Daemon.sh -down
```

Note: deactivating the APIs will not change or delete any data, it will simply stop communication with the server
