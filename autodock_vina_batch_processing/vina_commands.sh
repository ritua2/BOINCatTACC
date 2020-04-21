#!/bin/bash
#example showing how to run this script: ./vina_commands.sh <path-to-the-ligands-sub-directories> 5r80_apo.pdbqt 

cd $1
list_of_data_directories=$(ls -1d */)
#echo $list_of_data_directories;
RECEPTOR=$2

for j in $list_of_data_directories
 do
    trim_j=$(echo "${j%?}")
    echo "tar -xvzf $trim_j.tgz;cd $trim_j;" >> "$1/${trim_j}_mycommands.sh"
    cd $j;
    files=$(ls *.pdbqt);
    for i in $files
     do
       if [[ "$i" != "$RECEPTOR" ]]; then
         echo "vina --receptor $RECEPTOR --ligand $i --center_x 114 --center_y 121 --center_z 125 --size_x 30 --size_y 30 --size_z 30 --out out_$i >> ${trim_j}_log.txt ;" >> "$1/${trim_j}_mycommands.sh"   
       fi
     done

     tr -d '\n' < "$1/${trim_j}_mycommands.sh" > "$1/${trim_j}_mycommands2.sh"
     mv "$1/${trim_j}_mycommands2.sh" "$1/${trim_j}_mycommands.sh"
    
     echo -en '\n'  >> "$1/${trim_j}_mycommands.sh"
     chmod +x "$1/${trim_j}_mycommands.sh"
     
    cd ..
 done
