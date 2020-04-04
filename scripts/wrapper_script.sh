
#!/bin/bash

ls -1 $1/*.tgz| sed -e 's/\.tgz$//' > input_names.txt

cat input_names.txt | while read line 
do
   /scratch/03864/suman1/tacc/test_scripts/adv_automate_boinc_submit.sh $line.tgz ${line}_mycommands.sh
done
