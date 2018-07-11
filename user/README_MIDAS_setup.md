### BASICS

-----

**MIDAS**: **M**ultiple **I**nput **D**ocker **A**utomation **S**ystem


* **Comments**  
Lines starting with *#* are comments  
Lines starting with *//* are also comments  

* **README set-up**  
Each file contains the following sections (OS, language, packages, language libraries, set-up, secondary files, results). All of them
must be specified or the server will throw an error.  
Use colons to mark the start of a section, indentation will be ignored. Write each new result on a new line (including the first input.
Do not use dashed except when necessary for file names. Do not embed a section inside another. All libraries and packages required must be
entered in the order they have to be installed. In the case of packages, it can be assumed that the OS will start by updating the package manager
at the start of the container. 
The server will throw an error if any section is missing.  
If any section is to be left empty, write NONE instead.
The server will automatically process the results and extract them from BOINC.  
Do not attempt to send the results with anpther part of the program, access to the internet may not be allowed by the BOINC wrapper.  
Any error will result in a computational error, which will void the results and stop all processing.  

* **OS**  
The following OS are supported:
	* Ubuntu (14.04, 16.04, 17.10, 18.04)  
	* Debian (no accepted flavors, only the latest dockerfile is accepted)  
	* Alpine (no accepted flavors, only latest image will be accepted)  
	* CentOS (6, 7)  
	* NONE: Special case, assumes the Docker base image for the selected language, not valid for bash scripts. Use at own risk, image may be lacking packages that make it impossible to run the selected code
Windows and Mac operating systems are not accepted since they are, partially or completely, propietary software.  
FreeBSD is also not available since FreeBSD images are still not common.  

* **Language**  
The following languages are supported right now or will be covered in the future:
	* Python2, Python3: Select which version, Python willl refer to Python3 since 2 will be soon abandoned
	* Go/Golang
	* Fortran
	* Bash scripts (containing all the necessary commands for setup and running the program)
	* Haskell
	* OCaml
	* Elixir
	* Rust
	* C (using latest gcc version, no other compilers available)
	* C++ (using g++ version, no other compilers available)

It is possible to select more than one language to be used inside the container. But doing so will increase the size of the vbox wrapper. Languages
will be installed automatically inside the image. However, if there is only one language and the task is simple, consider using NONE as an OS.
Using NONE as OS is not allowed if more than one language is present.  

* **Packages**  
Enter all the packages that the OS will need to operate, with the exception of language packages. All packages must be easily installable
from the package manager (apt-get in the case of Ubuntu), for all others, use the set-up file. To compile from source, also use the
set-up file command.  

* **Language libraries**  
Enter the name of the all the necessary language libraries, if any library depends on another one, enter them in successive order. In the case of 
Fortran, C and C++, language libraries cannot be used as input. Instead, write them in the se-up file. 
For more than one language, write down the packages in the following form:  
{LANGUAGE} -> {Library}  
i.e. :  
	Python3 -> numpy  
	Go -> http-enumerator  
In all these cases, the program will use the standard language package manager: pip3 for python3, cabal for Haskell, etc.  

* **Set-Up**  
Provide the name of one and/or multiple bash script files containing the necessary setup before the program is run. Use this approach
when using C, C++, or Fortran libraries; or when compiling from source. This set-up will be initiated after the language and necessary
packages are installed. If providing more than one set-up file, enter them in order.  

* **Secondary Files**  
Enter the number of seconday files provided (do not include the README in it), starting by a *+* sign followed by the number.  
Enter the names of the seconday files. The server will check that all of them have been provided. If any is missing or the names
are not correct, it will throw an error.  

* **Results**
Enter the names of all the files in which your programs will be entering the results. Try to choose a name as specific as possible,
the server will automatically move these files when the job is complete and return them to the BOINC server. Do not name any of these files
as DPI.txt, since this contains information for database processing. Doing so will cause the server to throw an error.  
BOINC can only remove text files, and binary files for results are not guaranteed to run in another system. As such, only the following
file extensions will be accepted for outputs: .txt, .csv, .json .  
If want to provide another output, make sure that it is turned into an appropriate text file.

-------
------

### Examples
There are 2 examples available, one for python3 and another for C++ using the g++ compiler available at boincserver:
boincserver/MIDAS_example_c++.txt  
boincserver/README_MIDAS_example_python.txt
