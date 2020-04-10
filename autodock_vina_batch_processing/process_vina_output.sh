#to use, run the following command from the directory with out_*.pdbqt files: ./process_vina_output.sh 5r80_apo.pdbqt
#!/bin/sh

z=0
echo Line_Number,Receptor,Ligand,Score > receptor_ligand_score.csv
for a in `ls -1 *.pdbqt`
do
   x=$(echo `sed '4,4!d' $a| cut -f2 -d":"`)
   y=$(echo `sed '2,2!d' $a| cut -f2 -d":"| cut -c 6-10`)
   z=`expr $z + 1`
   echo $z,$1,$x,$y >> receptor_ligand_score.csv
done

echo Line_Number,Receptor,Ligand,Score > sorted_receptor_ligand_score.csv
sort -k4 -n -t, <(tail -n+2 receptor_ligand_score.csv) >> sorted_receptor_ligand_score.csv
cut -d, -f1 --complement sorted_receptor_ligand_score.csv > receptor_ligand_score.csv
awk '{printf "%s,%s\n", NR-1,$0}' receptor_ligand_score.csv > sorted_receptor_ligand_score.csv
rm receptor_ligand_score.csv
var="Line_Number,Receptor,Ligand,Score"
sed -i "1s/.*/$var/" sorted_receptor_ligand_score.csv
