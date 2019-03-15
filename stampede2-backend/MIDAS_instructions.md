### Automated Docker build instructions
-------




#### MIDAS overview

MIDAS (Multiple Input Docker Automation System) provides an automated way through which researchers can run custom codes in volunteered devices using the BOINC@TACC
infrastructure. MIDAS will automatically generate a Dockerfile based on the researcher's inputs, which will then be built into an image containing all the job
information. Should the build fail, an automated email will be sent to the researcher accounting for the error.
Succesful Dockerfiles will also be returned to the researchers via email.

MIDAS supports code written in the following languages: Bash, C, C++, Fortran, Python3, R.
All user-submitted codes are run on an Ubuntu 16.04 OS image.


#### Command Line Interface

The *advance-submit.sh* for the Stampede2 and Lonestar5 systems provide will guide the user should he wish to construct a Docker image (option 3). Simply follow the instructions presented at each step.



#### Web interface

1. Select the OS: Ubuntu 16.04
2. Select the programming language (one or more)
	* Only Python3 and C++ support automatic library downloads:
		* Python3 libraries will be installed using pip3
		* C++ libraries will be installed using [cget](https://github.com/pfultz2/cget), cget will be installed automatically. For a complete list of cget supported libraries, visit https://github.com/pfultz2/cget-recipes/tree/master/recipes . Users can also provide their own codes and *make install* using the setup file.
3. Provide a setup file (must be bash): Contains a list of commands run for the image creation. This file can contain compile instructions but must not run the job commands.
4. Provide a top and/or subtopic: Can be left empty.
5. Commands: Provide a list of commands, hit enter at the end of each line (including the last one)
6. Select which output files must be retrieved after the job complete, or select all of them by marking the appropriate icon.
7. Input the necessary files in either *.zip* or *.tar.gz* format.





