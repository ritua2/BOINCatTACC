#!/bin/bash

i=$1
list_of_pdqbt_files=$2
path_to_receptorfile=$3
mkdir -p data_"$i";
cp $path_to_receptorfile data_"$i";
j_START=$(( 25*i ));
j_END=25;
cat $list_of_pdqbt_files| head -n $j_START| tail -n $j_END > list_of_pdqbt_files_copied_$i.txt;

cat list_of_pdqbt_files_copied_$i.txt | while read line
        do
            cp $line data_"$i";
        done
find data_$i -type f -name "*.pdbqt" |xargs tar -czf data_$i.tgz
rm list_of_pdqbt_files_copied_$i.txt;
