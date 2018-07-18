#################################################
# Autodock-Vina image

# Largery based on TACC's taccsciapps/autodock-vina
# All commands are the same as the ones from the base image
# To obtain the results in the final folder, ismply run
# docker run carlosred/vintwo /bin/bash "command one; bash /Do_last.sh"
# License: Apache License 2.0

#################################################



FROM taccsciapps/autodock-vina


MAINTAINER Carlos Redondo <carlos.red@utexas.edu>
ENV _SECOND_AUTHOR "Carlos Redondo <carlos.red@utexas.edu"



# Copies the unaccounted files to /root/shared/results
COPY Mov_Res.py /Mov_Res.py

RUN mkdir -p /root/shared/results && touch /All_pdbqt.txt && mkdir -p /data &&\
    yum -y install wget; yum -y install  curl; yum -y install unzip; yum -y install tar &&\
	for afil in $(find /data -name '*'); do printf "$(readlink -e $afil)\n" >>  /All_pdbqt.txt; done


WORKDIR /data
