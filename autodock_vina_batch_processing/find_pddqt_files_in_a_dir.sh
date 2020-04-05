#sample command to use this script: ./find_pddqt_files_in_a_dir.sh ./ligands/AA ./prepared_jobs/AA_pdbqt.txt
#!/bin/bash
dir_path="$1"
outputfile="$2"
echo "input directory path->"  $dir_path
echo "output file name->" $outputfile
find $dir_path -name "*.pdbqt" > "$outputfile"
