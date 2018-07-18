#!/bin/bash

# Installs docker and erases the previous version
# Designed for programming convenience, should NOT be run otherwise

apt-get remove docker docker-engine docker.io
apt-get update

apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -


# Verifies correct key

ins_Key=$(apt-key fingerprint 0EBFCD88)

if [ *"9DC8 5822 9FC7 DD38 854A E2D8 8D81 803C 0EBF CD88"* != "$ins_key" ]; then

	printf "Invalid key, docker installation aborted\n"
	exit 0
fi


add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

apt-get update

apt-get install docker-ce


printf "Succesfully installed docker\n"

# Installs docker compsoe as well
curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

printf "Succesfully installed docker-compsoe\n"
