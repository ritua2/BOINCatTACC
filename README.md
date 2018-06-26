## Updates to the BOINC-Docker system created by [Marius Millea][1]



* user-interface: Creates a web interface to allow users to submit jobs more easily. Designed for slow, _personal_ interactions, not for APIs.
* api: Designed for large job batches.
* applications: Dockerized applications for BOINC usage, do not run in the server.
* stampede2-backend: Stampede2 connection, allows to establish a client for ieasier interaction with the server

To execute the jobs submitted through this server, download [BOINC][2] and Virtualbox if not installed already. Then, add the project using:  
*http://SERVER_IP/boincserver*  
The server will automatically recognize your system as a volunteer and submit tasks when they are available.  

-------

### Installation Guide  

0. **Install [Docker][3] and [Docker-compose][4] in their most recent versions** 

1. **Follow the installation instructions provided by [boinc-server-docker][1]**
	* Modify the *docker-compose.yml* to make it similar to the one provided in this repository. This updated compose file opens the ports 
	necessary for API usage. The only changes needed are in the ports for mysql and apache containers.
	* Most likely, this server will be installed on a cloud server. If that is the case, do not compose up directly. It is necessary to specify
	the IP of the system using the following syntax:
	* If not using root, it is possible that an error appears about Docker not being able to connect to the daemon. If this is the case, use 
	*sudo* to obtain root access, and use *sudo* for all docker and/or docker-compose commands.
```bash
	URL_BASE=http://IP_ADDRESS docker-compose up -d
```
	

2. **Wait a few seconds until the *make_project* container sets up the BOINC server and its mysql database**
	This process is complete when a webpage is accessible on *SERVER_IP/boincserver*

3. **Set-up basic administrative credentials**  
	* Execute *docker ps* do obtain all the data about the BOINC containers. If the setup is done correctly, there is an apache container.
	* Log into the apache container by using *docker exec -it {apache container ID} bash*
	* Follow to the guide in [BOINC HTMLOps][5] to set -up an administrative account with .htpasswd
		* .htpasswd is located in */root/project/html/ops*
	* Login into the administrative BOINC page at *SERVER_IP/boincserver_ops* with the username and password provided above

4. **Clone this repository**
	* If git is not installed, do it by executing: *apt-get update && apt-get install git-core -y*
	* If not already there, *cd /root/project*
	* Clone via: *git clone https://github.com/noderod/boinc-updates*
	* *cd boinc-updates*

5. **Establish user email credentials**
	* Run the appropriate bash script to set up the email and password
	* The basic set-up only allows for gmail, for all others, modify both *./api/preprocessing.py* and *./email_assimilator.py*
	* Be sure to have input the correct name and password, to change them again, change */root/.bashrc*
	* The same applies to the Docker, MIDAS credentials
	* Log out of the container and in again so the changes take effect
	Do:
```bash
	 bash password_credentials.sh
	 bash dockerhub_credentials.sh
	 exit
	 docker exec -it {APACHE SERVER} bash
```

6. **Run the setup file**  
	* It will install all the necessary packages, python libraries, set-up the internal Redis database, properly locate the files, set-up the APIs, Reef cloud storage, and automatic job processing
	* The set-up file will also automatically prompt to enter the credentials for the email. Use caution, since an error would require to manually fix the /root/.bashrc file
```bash
	 cd /root/project/boinc-updates
	 bash red_setup.sh
```


7. **Create organization acounts**  
	* 
	* A new token must be assigned to each new user (researcher who wants to submit BOINC jobs)
	* There are 2 options on assigning tokens:
		* Create one automatically through *create_token.py* (deprecated)
		* Create organization accounts
	* Organization accounts are preferred since they allow users to sign up in an easier way
	* Furthermore, users signing signing through this way will have to provide email authorization
	* To create an organization, following the instructions below and enter inputs accordingly
	* An automatic Reef account will be created for each user signing up through this method
	* For more instructions on supplying tokens through organizations, check the API documentation
	* To do this:
```bash
	cd /root/project/html/user/token_data
	python3 create_organization.py
```

[1]: https://github.com/marius311/boinc-server-docker
[2]: https://boinc.berkeley.edu/download.php
[3]: https://docs.docker.com/install/linux/docker-ce/ubuntu/
[4]: https://docs.docker.com/compose/install/
[5]: https://boinc.berkeley.edu/trac/wiki/HtmlOps


#### Future Use and Complains

1. Disconnecting the APIs, including Reef:
	* Disconnecting the APIs will not delete any files currently saved in Reef
```bash
	cd /root/project
	./API_Daemon.sh -down
```

2. Pulling the APIs up again:
```bash
	cd /root/project
	./API_Daemon.sh -up
```

3. I just submitted a job and it does not appear in the results ops page
	* boinc-docker-server needs to download the images before any further processing is done. For large images (> 1 Gb) this process can take time if the server has a low amount of RAM.

4. I received a job without an empty compressed results file  
Try to obtain your results in a regular file, since those are the files that our file retrieval tool supports. In general, use the general outputs
or texts files. Avoid images and binary files for results. Using plotting inside a BOINC job may cause problems, since most graphic libraries 
assume a screen.  
