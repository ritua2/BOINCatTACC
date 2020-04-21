# Copy the RECEPTOR file to the current working directory BEFORE running this script.
# For example, you should have the following receptor already available: 5r80_apo.pdbqt
# Run this script as follows: ./prepare_datadirectories.sh ./prepared_jobs/AA_pdbqt.txt ./prepared_jobs/5r80_apo.pdbqt
#!/bin/bash
list_of_pdqbt_files=$1
count=$(wc -l $1| cut -d" " -f1);
echo "Total number of PDBQT files at the provided path: $count";
num_subdir=`expr $count / 25`;
echo "Number of sub-directories to be created: $num_subdir";
path_to_receptorfile=$2
echo "Receptor file to be used: $path_to_receptorfile"
START=1
END=$num_subdir
for (( i=$START; i<=$END; i++ ))
 do
 	      mkdir -p data_"$i";
        cp $path_to_receptorfile data_"$i";
        j_START=$(( 25*i ));
        j_END=25;
        cat $list_of_pdqbt_files| head -n $j_START| tail -n $j_END > list_of_pdqbt_files_copied.txt;
        #cp list_of_pdqbt_files_copied.txt data_"$i";
        cat list_of_pdqbt_files_copied.txt | while read line
        do
            cp $line data_"$i";
        done
        find data_$i -type f -name "*.pdbqt" |xargs tar -czf data_$i.tgz
        rm list_of_pdqbt_files_copied.txt;
 done
