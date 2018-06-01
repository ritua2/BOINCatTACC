### Autodock-Vina Docker Image for BOINC usage

Largely based on <https://hub.docker.com/r/stevemock/docker-opensees/>

--------

**Instructions**  
Execute regular OpenSees commands separated by *;*.  
Add *python /Mov_Res.py* as the last command, this will move all the results (*.out* files) into the BOINC results folder. All
result files will have their file ending changed to *.txt* but their content will not be modified.
