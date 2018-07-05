#### ADTD-Protocol

*A simpler way to submit Docker tasks*  

**Serverless Results**  
The ADTD-Protocol (Automated Docker Task Distribition Protocol) provides an out-of-the box system to submit jobs from the BOINC server 
directly to the volunteers. This system will send a tar file containing the image on which the execute the job, a text file with the commands,
and another text file with information about the task itself.  
This allows to run BOINC jobs within Docker itself and obtain the results without Virtualbox or specific applications. In order to work, the
servers that will execute the results must obtain the client code.  
