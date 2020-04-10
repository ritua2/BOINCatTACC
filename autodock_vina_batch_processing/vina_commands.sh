#example showing how to run this script: ./vina_commands.sh ./prepared_jobs 5r80_apo.pdbqt 
# Please replace "./prepared_jobs" in this script with the exact and complete path to the prepared_jobs folder

#!/bin/bash
list_of_data_directories=$(ls -1d */)
#echo $list_of_data_directories;
RECEPTOR=$2

for j in $list_of_data_directories
 do
    trim_j=$(echo "${j%?}")
    echo "tar -xvzf $trim_j.tgz;cd $trim_j;" >> "./prepared_jobs/${trim_j}_mycommands.sh"
    cd $j;
    files=$(ls *.pdbqt);
    for i in $files
     do
       if [[ "$i" != "$RECEPTOR" ]]; then
         echo "vina --receptor $RECEPTOR --ligand $i --center_x -27.98 --center_y 2.54 --center_z 28.15 --size_x 50 --size_y 50 --size_z 50 --out out_$i >> ${trim_j}_log.txt ;" >> "./prepared_jobs/${trim_j}_mycommands.sh"   
       fi
     done

     tr -d '\n' < "./prepared_jobs/${trim_j}_mycommands.sh" > "./prepared_jobs/${trim_j}_mycommands2.sh"
     mv "./prepared_jobs/${trim_j}_mycommands2.sh" "./prepared_jobs/${trim_j}_mycommands.sh"
    
     echo -en '\n'  >> "./prepared_jobs/${trim_j}_mycommands.sh"
     
    cd ..
 done
