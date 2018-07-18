### Autodock-Vina Docker Image for BOINC usage

Largely based on <https://hub.docker.com/r/taccsciapps/autodock-vina/>

--------

**Instructions**  
Execute regular autodock-vina commands separated by *;*.  
Add *python /Mov_Res.py* as the last command, this will move all the results (*.pdbqt* files) into the BOINC results folder. All
result files will have their file ending changed to *.txt* but their content will not be modified.
