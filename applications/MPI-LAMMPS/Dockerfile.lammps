#################################################
# LAMMPS 

# Largery based on malramsay/lammps
# All commands are the same as the ones from the base image
# To obtain the results in the final folder, simply run
# License: Apache License 2.0

# WARNING: Allows 2 options: 
#                 |- lmp_mpi: Specific MPI version
#                 |- lmp_g++: Uses g++ with MPI
#
# Both versions are equivalent for simple tasks
#################################################


FROM malramsay/lammps
MAINTAINER Carlos Redondo <carlos.red@utexas.edu>
ENV _SECOND_AUTHOR "Carlos Redondo <carlos.red@utexas.edu"

# BOINC requires access to the /root/ folder
USER root


# Sets up the basic LAMMPS as well
RUN yum -y localinstall --nogpgcheck http://git.icms.temple.edu/rpm/centos/lammps-centos-rhel-repo-1-2.noarch.rpm &&\
    cd /etc/yum.repos.d/ &&\
    yum -y install lammps unzip

WORKDIR /data


# Installs realpath command so that the program can access the full path information of files


# Copies the unaccounted files to /root/shared/results
COPY Mov_Res.py /Mov_Res.py

# The python program will move the .png, .jpg, .jpeg, .txt files out


RUN mkdir -p /root/shared/results && touch /All_outs.txt &&\
	for afil in $(find /data -name '*.txt'); do printf "$(realpath $afil)\n" >>  /All_outs.txt; done &&\
	for afil in $(find /data -name '*.jpeg'); do printf "$(realpath $afil)\n" >>  /All_outs.txt; done &&\
	for afil in $(find /data -name '*.jpg'); do printf "$(realpath $afil)\n" >>  /All_outs.txt; done &&\
	for afil in $(find /data -name '*.png'); do printf "$(realpath $afil)\n" >>  /All_outs.txt; done
