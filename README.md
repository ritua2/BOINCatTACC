### BOINC@TACC project ###

This project provides a conduit for routing High-Throughput Computing (HTC) jobs from TACC resources to a BOINC server, and from there, to the BOINC clients (which run on volunteered hardware resources and VMs in the cloud). The project is funded through NSF Award #1664022.

This repository includes the following:

1) Front-end code for the BOINC@TACC website.
2) Scripts and API that run on the BOINC server for pulling job requests from TACC resources and pushing the requests to the BOINC clients.
3) A back-end script that can be run on TACC resources for determining if a job can be run on BOINC clients, or whether it should be run on TACC resources only.
4) A system for generating docker images from source code.
5) A mechanism for running BOINC jobs directly inside a Docker container instead of running them in VirtualBox. This is useful for institutional donors who may have volunteered VMs in the cloud.


### The project leverages the boinc-server-docker software developed by [Marius Millea][1]

Following folders are available in this repository:
* user-interface: Creates a web interface to allow researchers to submit and track jobs. 
* api: Designed for large job batches.
* applications: Dockerized applications for running on BOINC clients.
* stampede2-backend: A command-line interface for submitting BOINC jobs from the Stampede2 supercomputer at TACC. This script can be run on any Linux system that has the SLURM scheduler available. 

To execute the jobs submitted through the BOINC server, that is, to become a BOINC client, download [BOINC][2] and Virtualbox if not installed already. Then, add the project using the following (where SERVER_IP is the IP address of the BOINC server/project website):  

*http://SERVER_IP/boincserver*  

The BOINC server will automatically recognize your system as a volunteer and will submit jobs to it when they are available. This project was previously named as TACC-2-BOINC and hence, had a different project URL. Since July 30th 2018, the project is called BOINC@TACC, and the following URL can be used for adding the project to the BOINC client: http://boinc.tacc.utexas.edu

-------

### Installation Guide  

0. **Install [Docker][3] and [Docker-compose][4] in their most recent versions**  
Note: Both docker and docker-compose require sudo access, to avoid this problem:
```bash
sudo groupadd docker
sudo gpasswd -a $USER docker
# Log out/in to activate these changes
```


1. **Follow the installation instructions provided by [boinc-server-docker][1]**
	* Most likely, this server will be installed on a cloud server. If that is the case, do not compose up directly. It is necessary to specify
	the IP of the system using the syntax below.
	* If not using root, it is possible that an error appears about Docker not being able to connect to the daemon. If this is the case, use 
	*sudo* to obtain root access, and use *sudo* for all docker and/or docker-compose commands.
```bash
git clone https://github.com/ritua2/BOINCatTACC
cd BOINCatTACC/boinc-server-docker
docker-compose pull
# Enter the changes on the docker-compose
URL_BASE=http://IP_ADDRESS docker-compose up -d
```


2. **Wait a few seconds until the *make_project* container sets up the BOINC server and its mysql database**
	This process is complete when a webpage is accessible on *SERVER_IP/boincserver*

3. **Set-up basic administrative credentials**  
	* Execute *docker ps* do obtain all the data about the BOINC containers. If the setup is done correctly, there is an apache container.
	* Log into the apache container by using *docker exec -it {apache container ID} bash*
	* Follow  the guide in [BOINC HTMLOps][5] to set -up an administrative account with .htpasswd
		* .htpasswd is located in */home/boincadm/project/html/ops/*
	* Login into the administrative BOINC page at *SERVER_IP/boincserver_ops* with the username and password provided above
```bash
# Find the docker container
docker ps
docker exec -it boincserverdocker_apache_1 bash
cd /home/boincadm/project/html/ops/
htpasswd -c .htpasswd $NEWUSERNAME
```

4. **Clone this repository**
	* If git is not installed, do it by executing: *apt-get update && apt-get install git-core -y*
	* If not already there, *cd /home/boincadm/project*
	* Clone via: *git clone https://github.com/ritua2/BOINCatTACC*
	* *cd BOINCatTACC*
```bash
apt-get update && apt-get install git-core -y
cd /home/boincadm/project
git clone https://github.com/ritua2/BOINCatTACC
cd BOINCatTACC
#Edit project.inc - update the URL/IP address at line # 40 - define("SECURE_URL_BASE", "");
vi project/project.inc
```

5. **Establish user email credentials**
	* Run the appropriate bash script to set up the email and password
	* The basic set-up only allows for gmail, for all others, modify both *./api/preprocessing.py* and *./email_assimilator.py*
	* Be sure to have input the correct name and password, to change them again, change */root/.bashrc*
	* The same applies to the Docker, MIDAS credentials - MIDAS is a software component for creating docker images from source-code
	* Run the external Reef set-up to connect to an external container. The process is entirely automated and designed so that user files are stored in a different system.

	Do:
```bash
source password_credentials.sh
#exit from the Apache Docker container
exit
```

6. **Setup Reef in an external container**  
	* The following instructions are for normal Reef setup. If there is a need for scalable storage please refer to the steps listed under Distributed Reef.
	* Reef is the storage container where all user files (results or not) are stored
	* Switch to the pocket-reef directory inside the BOINCatTACC directory after exiting the Docker container, and follow some of these [instructions](./pocket-reef) on a system with the above IP and password provided above
	* Note: Reef can be setup on any server as long as its IP is accessible from the main server

````bash
#switch to the pocket-reef directory inside BOINCatTACC directory in the VM outside any Docker container
# if after exiting from the apache container you ar ein the boinc-server-docker directory, type cd ..
cd ..
cd pocket-reef
# Change the Reef key to the one that you typed in Step # 5
vi docker-compose.yml
# Build a new container for Reef
docker-compose up -d
# Enter container - replace $CONTAINER with container name - in our case it is pocketreef_reef_1
docker exec -it $CONTAINER bash
cd /reef
# Activate the APIs
./API_Daemon.sh -up
#Exit the Reef container
exit

````

**Distributed Reef setup**
- Distributed Reef is scalable version of Reef and is setup in two stages where the first stage is to setup reef manager node on the boinc VM itself.
- The second stage is to setup the storage node(s) on remote VM(s)
- Note: Distributed Reef can be setup on any server as long as its IP is accessible from the main server

Stage-1:
````bash
#switch to the pocket-reef-distributed directory inside BOINCatTACC directory in the VM outside any Docker container
# if after exiting from the apache container you ar ein the boinc-server-docker directory, type cd ..
cd ..
cd pocket-reef-distributed
# Enter the IP address of the VM in .env file
vi .env
# Change the Reef key to the one that you typed in Step # 5
vi docker-compose.yml
# Generate a self signed certificate for the manager node which is valid for 365 days
openssl req -newkey rsa:2048 -nodes -keyout keyfile.key -x509 -days 365 -out certfile.crt
# Build a new container for Reef
docker-compose up -d
# Enter container - replace $CONTAINER with container name - in our case it is pocketreef_reef_1
docker exec -it $CONTAINER bash
cd /reef
# Activate the APIs
./API_Daemon.sh -up
#Exit the Reef container
exit

````
Stage-2(storage container on remote VM):
````bash
# Clone this repository on the remote VM
git clone https://github.com/ritua2/BOINCatTACC
cd BOINCatTACC/pocket-reef-distributed/storage-node/
# Update the IP address of the storage node and define unique key for that container
vim Dockerfile
# Generate a self signed certificate for the storage node which is valid for 365 days
openssl req -newkey rsa:2048 -nodes -keyout keyfile.key -x509 -days 365 -out certfile.crt
# Build the image for storage node
docker build -t reef_storage:latest .
# Start the container on top of the image
docker run -d --name=pocket-reef_storage_reef_1 -p 3443:3443 -v reef_storage:/rdat reef_storage:latest
# Enter container - replace $CONTAINER with container name - in our case it is pocket-reef_storage_reef_1
docker exec -it $CONTAINER bash
cd /reef
# Activate the APIs
./API_Daemon.sh -up
#Exit the Reef container
exit

````


7. **Run the setup file from the Apache container**  
	* It will install all the necessary packages, python libraries, set-up the internal Redis database, properly locate the files, set-up the APIs, Reef cloud storage, and automatic job processing
	* The set-up file will also automatically prompt to enter the credentials for the email. Use caution, since an error would require to manually fix the /root/.bashrc file
```bash
docker exec -it boincserverdocker_apache_1 bash
cd /home/boincadm/project/BOINCatTACC
bash red_setup.sh

#set the recpatcha
#Follow the instructions at this link: https://boinc.berkeley.edu/trac/wiki/ProtectionFromSpam
```


8. **Create organization accounts**  
	 
	* A new token must be assigned to each new user (researcher who wants to submit BOINC jobs)
	* There are 2 options on assigning tokens:
		* Create one automatically through *create_token.py* (deprecated)
		* Create organization accounts
	* Organization accounts are preferred since they allow users to sign up in an easier way
	* Furthermore, users signing through this way will not have to provide further email authorization
	* To create an organization, following the instructions below and enter inputs accordingly
	* An automatic Reef account will be created for each user signing up through this method
	* Organizations themselves are required to submit jobs using the Stampede2 backend
	* Only one organization is needed. However, more can be created in order to separate and differentiate users
	* For more instructions on supplying tokens through organizations, check the API documentation
	* Always use organization name 'TACC' in order to avoid issues with the front-end
	* To do this:
```bash
cd /home/boincadm/project/BOINCatTACC/user-interface/token_data
python3 create_organization.py
```


9. **Assign VolCon credentials**  

	* [VolCon](./volcon-mirrors) is a distributed way of running jobs on the cloud based on docker, without requiring the BOINC client or VirtualBox
	* Although it can run on any system with an unique IP address (such as internal networks accessible from the main BOINC server), it is primarily designed for cloud servers
	* By default, the main BOINC server does not provide VolCon and so any jobs submitted to it will never be run
	* To create a VolCon network, run the following steps (bash commands below):
		1. Assign VolCon credentials: provide VolCon password
		2. Start VolCon network: In order for VolCon to be more effective, a large set of working nodes is required. Here will show how to manually run a simple mirror container.
		3. Assign Runner credentials: Multiple types of VolCon runners can be used at the same type (GPUs or not, different providers, etc). All runners within the same provided organization type are assumed to be similar and so they can be requested in such a way if the user wishes to.
		4. Implement VolCon runners by organization: The example here must be run within a VM, can be run on multiple machines without any changes.


	* Note: VolCon is an update over the previous ADTD-P system and, although both share many features, VolCon is not backwards compatible


```bash
# (1) Apache container

python3 /home/boincadm/project/BOINCatTACC/create_VolCon_distributors.py
```

```bash
# (2) Mirror server

git clone https://github.com/ritua2/BOINCatTACC
cd BOINCatTACC/volcon-mirrors

# Build the image, image is not available in dockerhub
docker build -t boinc_tacc/volcon-mirrors:latest .
docker run -d -p 7000:7000 -e "main_server=boinc.tacc.utexas.edu" \
       -e "volcon_key=mercury" boinc_tacc/volcon-mirrors:latest
```

```bash
# (3) Apache container

python3 /home/boincadm/project/BOINCatTACC/create_VolCon_clusters.py
```

```bash
# (4) Client server

git clone https://github.com/ritua2/BOINCatTACC
cd BOINCatTACC/volcon-clients
# Build the image, image is not available in dockerhub
docker build -t boinc_tacc/volcon-clients:latest .
# Set GPU=1 to allow GPU jobs, set as 0 as default
# Set np to change the number of processes, default is 4 (i.e. np=8, 8 processes)
# Set only_public=1 to disallow MIDAS jobs, allowed by default
docker run -d -p 8000:8000 -e "main_server=boinc.tacc.utexas.edu" \
       -e "cluster=andromeda" -e "cluster_key=m110" -e "GPU=1" \
       --privileged -v /var/run/docker.sock:/var/run/docker.sock boinc_tacc/volcon-clients:latest
```


[1]: https://github.com/marius311/boinc-server-docker
[2]: https://boinc.berkeley.edu/download.php
[3]: https://docs.docker.com/install/linux/docker-ce/ubuntu/
[4]: https://docs.docker.com/compose/install/
[5]: https://boinc.berkeley.edu/trac/wiki/HtmlOps


#### Future Use and Complains

1. Disconnecting the APIs, including Reef - NOTE FROM RITU  - THESE COMMANDS ARE NOT CURRENTLY WORKING AS EXPECTED:
	* Disconnecting the APIs will not delete any files currently saved in Reef
```bash
cd /home/boincadm/project
./API_Daemon.sh -down
```

2. Pulling the APIs up again:
```bash
cd /home/boincadm/project
./API_Daemon.sh -up
```

3. I just submitted a job and it does not appear in the results ops page
	* boinc-docker-server needs to download the images before any further processing is done. For large images (> 1 Gb) this process can take time if the server has a low amount of RAM.

4. I received a job with an empty compressed results file  
Try to obtain your results in a regular file, since those are the files that our file retrieval tool supports. In general, use the general outputs
or texts files. Avoid images and binary files for results. Using plotting inside a BOINC job may cause problems, since most graphic libraries 
assume a screen.  


----------------

### Licensing


The OpenFOAM6 application that researchers can run through BOINC is licensed under GPL. 

This application is built [in container form](./applications/OpenFOAM6/Dockerfile), with the only change being [a python script](./applications/OpenFOAM6/Mov_Res.py) that moves the output results so that the BOINC client may return them to the server

A copy of the original GPLv3 license is provided [here](./applications/LICENSES), users may also find it in the OpenFOAM6 main Github [repository](https://github.com/OpenFOAM/OpenFOAM-6/blob/master/COPYING).

The OpenSees application that researchers can run through BOINC is licensed by the The Regents of the University of California, a copy of the original
copyright notice is included in this project [here](./applications/LICENSES/OpenSees_COPYRIGHT) or in its original
[Github Directory location](https://github.com/OpenSees/OpenSees/blob/master/COPYRIGHT).

