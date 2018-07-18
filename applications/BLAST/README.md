### BLAST Image for BOINC usage

Largely based on <https://hub.docker.com/r/biocontainers/blast/>

--------

**Instructions**  
Execute regular blast commands separated by *;*.  
Add *python /Mov_Res.py* as the last command, this will move all the results (*.txt*, *.jpg*, *.jpeg*, *.png* files) into the BOINC results folder.
  
All actions must be done within the */data* directory, set the absolute paths accordingly. 