### MIDAS guide

**Set-up**  
MIDAS (Multiple Input Docker Automation System) is a TACC tool designed for automatic dockerization. To use this tool, use the MIDAS API to submit either a *.tgz* or a *tar.gz* file containing all the necessary files.  
This tar file must only contain the files and subdirectories, not the directory that contains them all. For example, if the files are 
*f1.txt* and *f2.txt* inside the directory *midtest*, then the tar command would be *tar -cvzf TAR_FINAL_FILE.tar.gz .* within the *midtest*
directory.  
All files to be used must be inside, as well as a README.txt (required name, files without it will return an error) containing the set-up information.  
Users may assume root access.  
To do so, use:
 ```bash
 	curl -F midas_file=@MY_COMPRESSED_FILE.tgz http://SERVER_IP:5085/v2/midas_job/token=TOKEN
 ```

#### README.txt 

Required for MIDAS processing, it has 4 required sections (OS, LANGUAGE, COMMAND, OUTPUT) and two optionals (LIBRARY, USER_SETUP).  
The absence of any of the required sections will raise an error, and keep the user from continuing.  
Lines starting with *#* are comments. Same-line comments are not allowed.  The use of any OS or language not supported requires the user to create a set-up file.  Users are responsible to make sure that their programs run succesfully with files only allowed in local directories.  
The API will enforce that all referenced files (set-up and command files) are present.  
File names cannot have spaces, use underscores or dashes instead.  
For examples for README.txt, 2 will be provided in this same directory: python, C++ and setup file.  

**Order of Operations**  
All BOINC jobs submitted through MIDAS will be executed in the image in the following order:  
1. OS installation (base image selection)
2. Language installation
3. User set-up
4. Library installation
5. Commands
6. Results retrieval


**OS**  
Refers to the base OS on which all the other commands are run. 
Introduced by:
*[OS]*  
The following OS are supported, and they are written as:
Ubuntu 16.04
```
	[OS] Ubuntu_16.04
```

**Languages**  
The languages supported by the program, more than one language may be used. The following languages are supported as of now and installed automatically:  
	* Python (3) (Only python3 is supported, included by default)  
	* Fortran (90) (gfortran)  
	* R  
	* C (gcc)  
	* C++ (g++)  
	* Bash  

Each language is installed together with their package manager. The version installed for each language is the default used in the package manager. To use any custom manager, add the instructions in the setup file.  
For the sake of future use, both python and python3 refer to python3 (same with pip), whereas python2 refers to python2. Python3 is always installed, since it is needed to recover the results for BOINC.    
Bash is also installed by default.

To add a new language, do:
```
	[LANGUAGE] python
	[LANGUAGE] C++
```

**Libraries (Optional)**  
Language libraries, installed in the order that the user provides. If they cannot be installed directly, add the explicit instructions in the
set-up file. All libraries must be preceded by the language they support.  BOINC does not support software which requires a license or monetary
cost to be used.  
The name of the library must also be the name of the library when it is installed. This name may differ from the one used when it is called. For C++ libraries installed through cget, use the cget name, not the conventional one.  
In the case of C/C++; we will use the cget package manager because of its simplicity, This means that only packages available from buckarooo
will be automatically set-up for the user. For all others, it is necessary to specify the build process directly in the set-up file.  
Libraries will be installed via the default package manager (pip for python, cargo for Rust, etc).  
Note: There are certain libraries (basemap in python, for example) that require a specific setup. These libraries cannot be setup in this command
and the user must do so in the set-up file.  
In the case of C, Fortran, and C++, the user must specify the install and set-up the appropriate paths using the set-up file.  
Not all languages support automatic libraries. So far, only python, Haskell, and (to a lesser extent) C++ do. For the others, no libraries can
be installed using MIDAS. They must be installed within a setup file (which must be a bash script). If the user, however, provides a library using the *LIBRARY)* syntax, it will return an error.  
To add a library, select the language first and then the language with the following syntax:
```
	[LIBRARY] python: boost
	[LIBRARY] C++ cget: boost
```

**Set-up (Optional)**  
Specially useful for C and C++.  
Allows the user to provide a set of bash scripts (MUST be bash scripts, ending in *.sh*) that either install new programs or set-up paths.  
The user must make sure that the syntax is correct, otherwise the build will raise an error.  
Makefiles in particular must be set-up using a set-up file.  
In general, avoid using user setup as much as possible, since it increases the size of the image. For all setup that does not require network
access (package installation, curl, wget, ...) submit the instructions in a bash script executable with the *COMMAND* focus.  
More than one set-up file will be allowed but they will be executed in the order they are present.  
NOTE: Contrary to the command input files, the server will not check that the set-up files are present, so the user is responsible to make sure
that they are present.  
NOTE: Do not execute job commands in the set-up, since this would not make use of BOINC at all.  
Use the following syntax:  
```
	[USER_SETUP] file_setup1.sh
	[USER_SETUP] file_setup2.sh
```

**Command**  
The actual command, to be executed. Requires the syntax LANGUAGE: FILE.  Only one file may be issued after the command. All commands must be done using this syntax, so plan accordingly. MIDAS will check that all input files are present before running the command.  
means no arguments in the command line. If you request specific commands, put them in a text file, include that file, and make the program read it.  
It is also possible to use the bash command on bash files as a command, so that multiple instructions can be executed at the same time.  
All output printed to the terminal will be lost since BOINC is not designed for an user interface for jobs.  
In the case of scripted languages, the image will just execute the command.  
For compiled languages, the image will first compile the file using the language's default compiler (gcc for C, etc) and then run the executable.
For C++ libraries installed using buckaroo, MIDAS will automatically set the -I flags to set-up the necessary libraries.  
For both C and C++, the program gives the suer liberty to locate the libraries and commands before or after the file, use *_1_* and
*_2_* markers to denote previous and afterwards, respectively
The program assumes that the user knows how to properly use file extensions, so it will not raise an error if they do not match the language.  
This form is, as of now, the only one available, only language commands may be executed.  

* *R*  
	R requires a 3 step command structure, otherwise it will just print to console and the results will not be retrieved. To specify the end
	file to where print the results, do as below.  The R version provided is *r-base*, if you desire a more recent version, install it with the
	set-up functionality and change the necessary paths.  
	R also does not accept libraries from terminal, to install libraries, add them in the set-up script.    

* *C*  
	C requires a multiple command structure to specify which libraries will be used in a C program. The libraries will be added with the -I flag.
	Libraries must be provided with the path starting at the local level (no */* in front of them). If the libraries are installed with
	*make install*, however, it may not be necessary to specify the path if the setup does already.   
* *C++*  
	C++ requires a multiple command structure to specify which libraries will be used in a C program. The libraries will be added with the -I
	flag. Since cget contains a large amount of files (although definitely less than 15 MB), there are 2 options for C++: C++/C++ cget. C++ does
	not allow cget usage and follows the same steps for library installation that C does. C++ cget requires installation and so it can take
	significantly longer.
	However, set-up is easier. For cget libraries, start the library call with the start library within the C++ file, i.e.:  
		*#include <boost/numeric/ublas/matrix.hpp>* intead of */numeric/ublas/matrix.hpp*  
		*#include <eigen2/Eigen/Dense>* instead of *#include <Eigen/Dense>*
	Libraries installed through cget (using the *LIBRARY)* command) do not require any setup. They are always setup **in front of**
	the file to be compiled.  


Use the syntax:  
```
	[COMMAND] python: brain_analysis.py
	# python brain_analysis.py
	[COMMAND] R: call_center.R: results_center.txt
	# Rscript call_center.R > results_center.txt
	[COMMAND] C: small_eigen.c: eigen-eigen-5a0156e40feb/Eigen/Dense
	# gcc -I eigen-eigen-5a0156e40feb/Eigen/Dense small_eigen.c -o a.out && a.out
	[COMMAND] C++: MRI_scanner.cpp
	# g++ MRI_scanner.cpp -o a.out && a.out
	[COMMAND] C++ cget: vertebra.cpp: _CGET
	# g++ -I CGETPATH/ vertebra.cpp -o a.out && a.out // cget will setup the appropriate paths for all installed libraries above
```

**Output Files**
Output files that will be recovered by the BOINC server. Everything not included as output will NOT be recovered, so be careful with the
selection. Alternatively, users may select *ALL* to recover everything in the working directory. This may cause problems with BOINC, since
recovering binary files can sometimes cause problems.
```
	# Will recover all files in the /work/ directory, without distinction
	[OUTPUT] ALL
```
```
	# Will recover only out1.txt and spinal_analysis.txt
	[OUTPUT] out1.txt
	[OUTPUT] spinal_analysis.txt
```

--------

#### Where is each process executed?

* **OS, language and package installation, set-up**: BOINC server  
The server will provide the user with a new Docker image that will be pushed to Dockerhub and erased from the server immediately after build. If the build fails, the MIDAS API will return an error message.

* **Commands**: Volunteer computer  
All commands are executed in the volunteers, any errors arising there will most likely result in a computational error, which the user will not
receive until crash. This will not be available immediately and could take days to occur, as soon as the volunteer is done.

---------

#### Common Issues  

* **Errors in plotting and graphics**  
Most graphical libraries are designed to work with a screen in mind (take matplotlib, for example). If this is not the case, such as in BOINC, then the program will return an error and keep the job from being completed. MIDAS does not check for these types of errors and it is up to
the user to correct them.  
Bear in mind that that an error of this type would not be an image buuild error and so it would be the BOINC job that would fail, not the 
image build. The user would, then, only be notified after the volunteer cannot run the job.  
