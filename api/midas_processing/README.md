### MIDAS guide

**Set-up**  
MIDAS (Multiple Input Docker Automation System) is a TACC tool designed for automatic dockerization. To use this tool, use the MIDAS API to submit either a *.tgz* or a *tar.gz* file containing all the necessary files.  
This tar file must only contain the files and subdirectories, not the directory that contains them all. For eacample, if the files are 
*f1.txt* and *f2.txt* inside the directory *midtest*, then the tar command would be *tar -cvzf TAR_FINAL_FILE.tar.gz .* within the *midtest*
directory.  
All files to be used must be inside, as well as a README.txt (required name, files without it will return an error) containing the set-up information.  
Users may assume root access.  
To do so, use:
 ```bash
 	curl -F midas_file=MY_COMPRESSED_FILE.tgz http://SERVER_IP:5085/v2/midas_job/token=TOKEN
 ```

#### README.txt 

Required for MIDAS processing, it has 4 required sections (OS, LANGUAGE, COMMAND, OUTPUT) and two optionals (LIBRARY, USER_SETUP).  
The absence of any of the required sections will raise an error, and keep the user from continuing.  
Lines starting with *H* are comments. Same-line comments are not allowed.  The use of any OS or language not supported requires the user to create a set-up file.  Users are responsible to make sure that their programs run succesfully with files only allowed in local directories.  
The API will enforce that all referenced files (set-up and command files) are present.  
File names cannot have spaces, use underscores or dashes instead.  
For examples for README.txt, 2 will be provided in this same directory: python, C++ and setup file.

**OS**  
Refers to the base OS on which all the other commands are run. 
Introduced by:
*OS)*  
The following OS are supported, and they are written as:
Ubuntu 16.04
```
	OS) Ubuntu_16.04
```

**Language**  
The languages supported by the program, more than one language may be used. The following languages are supported as of now and installed automatically:
	* Python (3) (Only python3 is supported, included by default)
	* Fortran (gfortran)
	* R
	* Haskell
	* C (gcc)
	* C++ (g++)

Each language is installed together with their package manager or. The version installed for each language is the default used in the package manager. To use any custom manager, add the instruuctions in the setup file.  
For the sake of future use, both python and python3 refer to python3 (same with pip), whereas python2 refers to python2. Python3 is always installed, since it is needed to recover the results for BOINC.    
Bash is also installed by default.
To add a new language, do:
```
	LANGUAGE) python
	LANGUAGE) C++
```

**Libraries (Optional)**  
Language libraries, installed in the order that the user provides. If they cannot be installed directly, add the explicit instructions in the
set-up file. All libraries must be preceded by the language they support.  BOINC does not support software which requires a license or monetary
cost to be used.  
The name of the library must also be the name of the library when it is installed. This name may differe from the one used when it is called. For C++ libraries installed through buckaroo, use the buckaroo name, not the conventional one.  
In the case of C/C++; we will use the buckaroo package manager because of its simplicity, This means that only packages available from buckarooo
will be automatically set-up for the user. For all others, it is necessary to specify the build process directly in the set-up file.  
Libraries will be installed via the default package manager (pip for python, cargo for Rust, etc).  
Note: There are certain libraries (basemap in python, for example) that require a specific setup. These libraries cannot be setup in this command and the suer must do so in the set-up file.  
In the case of C, Fortran, and C++, the user must specify the install and set-up the appropriate paths using the set-up file.  
To add a library, select the language first and then the language with the following syntax:
```
	LANGUAGE) python
	LANGUAGE) C++
```

**Set-up (Optional)**  
Specially useful for C and C++.  
Allows the user to provide a set of bash scripts (MUST be bash scripts, ending in *.sh*) that either install new programs or set-up paths.  
The user must make sure that the syntax is correct, otherwise the build will raise an error.  
Makefiles in particular must be set-up using a set-up file.  
More than one set-up file will be allowed but they will be executed in the order they are present.  
NOTE: Contrary to the command input files, the server will not check that the set-up files are present, so the suer is responsible to make sure
that they are present.  
Use the following syntax:  
```
	USER_SETUP) file_setup1.sh
	USER_SETUP) file_setup2.sh
```

**Command**  
The actual command, to be executed. Requires the syntax LANGUAGE: FILE.  Only one file may be issued after the command. All commands must be done using this syntax, so plan accordingly. This
means no arguments in the command line. If you request specific commands, put them in a text file, include that file, and make the program read it.  
In the case of scripted languages, the image will just execute the command.  
For compiled languages, the image will first compile the file using the language's default compiler (gcc for C, etc) and then run the executable.
For C++ libraries installed using buckaroo, MIDAS will automatically set the -I flags to set-up the necessary libraries.    
The program assumes that the user knows how the file extensions, so it will not raise an error if they do not match the language.  
This form is, as of now, the only one available, only language commands may be executed.  
Use the syntax:  
```
	COMMAND) python:brain_analysis.py
	# python brain_analysis.py
	COMMAND) C++:MRI_scanner.cpp
	# g++ MRI_scanner.cpp -o MRI_scanner.out && MRI_scanner.out
	COMMAND) Go:spinal.go
	# go run spinal.go
```

**Output Files**
Output files that will be recovered by the BOINC server. Everything not included as output will NOT be recovered, so be careful with the
selection. Alternatively, users may select *ALL* to recover everything in the working directory. This may cause problems with BOINC, since
recovering binary files can sometimes cause problems.
```
	# Will recover all files in the /work/ directory, without distinction
	OUTPUT) ALL
```
```
	# Will recover only out1.txt and spinal_analysis.txt
	OUTPUT) out1.txt
	OUTPUT) spinal_analysis.txt
```


#### Where is each process executed?

* **OS, language and package installation, set-up**: BOINC server
The server will provide the user with a new Docker image that will be pushed to Dockerhub and erased from the server immediately after build. If the build fails, the MIDAS API will return an error message.

* **Commands**: Volunteer computer
All commands are executed in the volunteers, any errors arising there will most likely result in a computational error, which the user will not
receive until crash. This will not be available immediately and could take days to occur, as soon as the volunteer is done.
