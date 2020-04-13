#run this script from the directory that contains the boinc@tacc results *.tgz files that need to be extracted
#!/bin/bash

counter=0
for a in `ls -1`
 do 
        ls -1 *.tgz | xargs -n1 tar -xzf; 
        ((counter=counter+1))
	if [ $counter -eq 100 ]
	then
		mkdir -p out_$counter
		mv out_* out_$counter/.
		((counter=0))
        fi
	
 done

