#Example to show how to use this script: ./wrapper_script.sh ./test_scripts/data_4
#!/bin/bash
ls -1 $1/*.tgz| sed -e 's/\.tgz$//' > input_names.txt

cat input_names.txt | while read line 
do
   ./test_scripts/adv_automate_boinc_submit.sh $line.tgz ${line}_mycommands.sh
done
