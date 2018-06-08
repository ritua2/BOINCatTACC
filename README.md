## Updates to the BOINC-Docker system created by [Marius Millea][1]



* user-interface: Creates a web interface to allow users to submit jobs more easily. Designed for slow, _personal_ interactions, not for APIs.
* api: Designed for large job batches.
* applications: Dockerized applications for BOINC usage, do not run in the server.
* stampede2-backend: Stampede2 connection, allows to establish a client for ieasier interaction with the server


[1]: https://github.com/marius311/boinc-server-docker

-------

### Installation Guide  

0. **Install [Docker][2] and [Docker-compose][3] in their most recent versions** 

1. **Follow the installation instructions provided by [boinc-server-docker][1]**
	* Modify the *docker-compose.yml* to make it similar to the one provided in thsi repository. This updated compose file opens the ports 
	necessary for API usage.
	* Most likely, this server will be installed on a cloud server. If that is the case, do not compose up directly. It is necessary to specify
	the IP of the system using the following syntax:
		*URL_BASE=http://IP_ADDRESS docker-compose up -d*
	* If not using root, it is possible that an error appears about Docker not being able to connect to the daemon. If this is the case, use 
	*sudo* to obtain root access, and use *sudo* for all docker and/or docker-compose commands.

2. **Wait a few seconds until the *make_project* container sets up the BOINC server and its mysql database**
	This process is complete when a webpage is accessible on *SERVER_IP/boincserver*

3. **Set-up basic administrative credentials**  
	* Execute *docker ps* do obtain all the data about the BOINC containers. If the setup is done correctly, there is an apache container.
	* Log into the apache container by using *docker exec -it {apache container ID} bash*
	* Follow to the guide in [BOINC HTMLOps][4] to set -up an administrative account with .htpasswd
	* .htpasswd is located in */root/project/html/ops*
	* Login into the administrative BOINC page at *SERVER_IP/boincserver_ops* with the username and password provided above

4. **Clone this repository**
	* If git is not installed, do it by executing: *apt-get update && apt-get install git-core -y*
	* If not already there, *cd /root/project*
	* Clone via: *git clone https://github.com/noderod/boinc-updates*
	* *cd boinc-updates*

5. **Change the mysql database and email credentials in email_assimilator.py**
	* Use an organization email for better use
	* Email frequency is specified as a cron job in */root/project/bproc.sh* as is set up to each 30 minutes by default
	* The mysql password has root user for BOINC by default
	* The mysql connector IP must be specified to the same IP as the server itself

6. **Run the setup file**
	* *bash red_setup.sh*
	* It will install all the necessary packages, python libraries, set-up the internal Redis database, properly locate the files, set-up the APIs, Reef cloud storage, and automatic job processing.

7. **Create user tokens**
	* A new token must be assigned to each new user (researcher who wants to submit BOINC jobs)
	* To do this: *cd /root/project/html/user/token_data*
		*python3 create_token FIRST_NAME LAST_NAME EMAIL*
	* Tokens allow access to manual job submission, APIs and Reef cloud storage
	* For more instructions on Reef usage, go to the api README in this repository


[2]: https://docs.docker.com/install/linux/docker-ce/ubuntu/
[3]: https://docs.docker.com/compose/install/
[4]: https://boinc.berkeley.edu/trac/wiki/HtmlOps


#### Future Use and Complains

1. Disconnecting the APIs, including Reef:
	*cd /root/project; ./API_Daemon.sh -down*
	* Disconnecting the APIs will not delete any files currently saved in Reef

2. Pulling the APIs up again:
	*cd /root/project; ./API_Daemon.sh -up*

3. I just submitted a job and it does not appear in the results ops page
	* boinc-docker-server needs to download the images before any further processing is done. For large images (> 1 Gb) this process can take time if the server has a low amount of RAM.
