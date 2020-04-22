#!/bin/bash
task(){
   count=0
   while IFS= read -r line
    do
    if [[ $line == ATOM* ]]; then
     x_coord=` echo “$line” | awk ‘{print $6}’ `
     y_coord=` echo “$line” | awk ‘{print $7}’ `
     z_coord=` echo “$line” | awk ‘{print $8}’ `
     if [ “$x_coord” = “0.000” ] && [ “$y_coord” = “0.000” ] && [ “$z_coord” = “0.000” ]
      then
      count=$((count+1))
      if [[ $count == 2 ]]
       then
       echo $1
      # echo $1 >> list_of_bad_files.txt
       break
      fi
     fi
    fi
   done < $1
}
declare -a dir_list
dir_list=` find ./ -type d -name ‘data*’ `
for i in ${dir_list[@]}; do
 declare -a file_list
 file_list=` find $i -type f -name ‘*pdbqt’ | grep -v apo `
 for k in ${file_list[@]}; do
  task $k &
 done
done
