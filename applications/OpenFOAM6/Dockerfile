#################################################
# OpenFOAM6 image designed for BOINC

# All commands are the same as the ones from the base image

#################################################



FROM richardlock/openfoam6-paraview54-intelmpi:latest

MAINTAINER Carlos Redondo <carlos.red@utexas.edu>
ENV _SECOND_AUTHOR "Carlos Redondo <carlos.red@utexas.edu"
# Because the previous user is Ubuntu and BOINC requires access to the /root/ folder
USER root

# All jobs can be safely assumed to be run inside
ENV FOAM_RUN="/data"

COPY Mov_Res.py /Mov_Res.py

WORKDIR /data


# Makes python synonym with python3 for simplicty
RUN cp /usr/bin/python3 /usr/bin/python && mkdir -p "/root/shared/results" && rm -rf /opt/OpenFOAM/OpenFOAM-6/tutorials/ \
	/opt/OpenFOAM/OpenFOAM-6/doc/ 


# Requires the command
# source /opt/OpenFOAM/OpenFOAM-6/etc/bashrc
