# Run this script as follows: ./prepare_datadirecotries.sh ./prepared_jobs/AA_pdbqt.txt ./prepared_jobs/5r80_apo.pdbqt
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

echo "$START" > read_from.txt
echo "$END" >> read_from.txt
echo "$path_to_receptorfile" >> read_from.txt
