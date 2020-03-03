### Job submission through Stampede2
-------


#### **Prerequisites**  
Instructions below should be run from Stampede2 or Lonestar5 supercomputers  



#### **Installation**  
Obtain the required files from [this directory](./S2-test-files):


```bash
svn checkout https://github.com/ritua2/BOINCatTACC/trunk/stampede2-backend/S2-test-files
cd S2-test-files
chmod +x advance-submit.sh
```


#### **Accessing the tutorial files for specific applications**

A sample exercise for each specific application is provided below. All the necessary files are available when cloning the github repo as per the above
instructions. However, for users wishing to use only one application, follow the instructions below:

* BOINC job submission

```bash

curl -O https://raw.githubusercontent.com/ritua2/BOINCatTACC/master/stampede2-backend/advance-submit.sh
chmod +x advance-submit.sh
```


1. AutoDock-Vina 

```bash
curl -O https://raw.githubusercontent.com/ritua2/BOINCatTACC/master/stampede2-backend/S2-test-files/protein.pdbqt
curl -O https://raw.githubusercontent.com/ritua2/BOINCatTACC/master/stampede2-backend/S2-test-files/protein.pdb
curl -O https://raw.githubusercontent.com/ritua2/BOINCatTACC/master/stampede2-backend/S2-test-files/ligand.pdbqt
curl -O https://raw.githubusercontent.com/ritua2/BOINCatTACC/master/stampede2-backend/S2-test-files/ligand.pdb
curl -O https://raw.githubusercontent.com/ritua2/BOINCatTACC/master/stampede2-backend/S2-test-files/ligand_experiment.pdbqt
curl -O https://raw.githubusercontent.com/ritua2/BOINCatTACC/master/stampede2-backend/S2-test-files/conf.txt
```


2. Bedtools

```bash
curl -O https://raw.githubusercontent.com/ritua2/BOINCatTACC/master/stampede2-backend/S2-test-files/cpg.bed
curl -O https://raw.githubusercontent.com/ritua2/BOINCatTACC/master/stampede2-backend/S2-test-files/exons.bed
```


3. Blast

```bash
curl -O https://raw.githubusercontent.com/ritua2/BOINCatTACC/master/stampede2-backend/S2-test-files/P04156.fasta
curl -O https://raw.githubusercontent.com/ritua2/BOINCatTACC/master/stampede2-backend/S2-test-files/zebrafish.1.protein.faa.gz
```



4. Bowtie

```bash
curl -O https://raw.githubusercontent.com/ritua2/BOINCatTACC/master/stampede2-backend/S2-test-files/s_cerevisiae.ebwt.zip
```



5. Gromacs

```bash
curl -O https://raw.githubusercontent.com/ritua2/BOINCatTACC/master/stampede2-backend/S2-test-files/methane_water.gro
curl -O https://raw.githubusercontent.com/ritua2/BOINCatTACC/master/stampede2-backend/S2-test-files/topol.top
curl -O https://raw.githubusercontent.com/ritua2/BOINCatTACC/master/stampede2-backend/S2-test-files/em_steep.mdp
```


6. HTseq

```bash
curl -O https://raw.githubusercontent.com/ritua2/BOINCatTACC/master/stampede2-backend/S2-test-files/test.sam
curl -O https://raw.githubusercontent.com/ritua2/BOINCatTACC/master/stampede2-backend/S2-test-files/gen.gtf
```



7. MPI-LAMMPS

```bash
curl -O https://raw.githubusercontent.com/ritua2/BOINCatTACC/master/stampede2-backend/S2-test-files/Al99.eam.alloy
curl -O https://raw.githubusercontent.com/ritua2/BOINCatTACC/master/stampede2-backend/S2-test-files/aluminium.in
```



8. NAMD

```bash
curl -O https://raw.githubusercontent.com/ritua2/BOINCatTACC/master/stampede2-backend/S2-test-files/alanin.psf
curl -O https://raw.githubusercontent.com/ritua2/BOINCatTACC/master/stampede2-backend/S2-test-files/alanin.conf
curl -O https://raw.githubusercontent.com/ritua2/BOINCatTACC/master/stampede2-backend/S2-test-files/alanin.pdb
curl -O https://raw.githubusercontent.com/ritua2/BOINCatTACC/master/stampede2-backend/S2-test-files/alanin.params
```



9. OpenSees

```bash
curl -O https://raw.githubusercontent.com/ritua2/BOINCatTACC/master/stampede2-backend/S2-test-files/MC.tcl
```



10. CUDA

```bash
curl -O https://raw.githubusercontent.com/ritua2/BOINCatTACC/master/stampede2-backend/S2-test-files/happ.cu
```



11. OpenFOAM6 (currently in testing)

```bash
mkdir 0 constant system
curl https://raw.githubusercontent.com/ritua2/BOINCatTACC/master/stampede2-backend/S2-test-files/0/U > 0/U
curl https://raw.githubusercontent.com/ritua2/BOINCatTACC/master/stampede2-backend/S2-test-files/0/p > 0/p
curl https://raw.githubusercontent.com/ritua2/BOINCatTACC/master/stampede2-backend/S2-test-files/constant/transportProperties > constant/transportProperties
mkdir constant/polyMesh
curl https://raw.githubusercontent.com/ritua2/BOINCatTACC/master/stampede2-backend/S2-test-files/constant/polyMesh/boundary  > constant/polyMesh/boundary
curl https://raw.githubusercontent.com/ritua2/BOINCatTACC/master/stampede2-backend/S2-test-files/constant/polyMesh/faces     > constant/polyMesh/faces
curl https://raw.githubusercontent.com/ritua2/BOINCatTACC/master/stampede2-backend/S2-test-files/constant/polyMesh/neighbour > constant/polyMesh/neighbour
curl https://raw.githubusercontent.com/ritua2/BOINCatTACC/master/stampede2-backend/S2-test-files/constant/polyMesh/owner     > constant/polyMesh/owner
curl https://raw.githubusercontent.com/ritua2/BOINCatTACC/master/stampede2-backend/S2-test-files/constant/polyMesh/points    > constant/polyMesh/points
curl https://raw.githubusercontent.com/ritua2/BOINCatTACC/master/stampede2-backend/S2-test-files/system/blockMeshDict        > system/blockMeshDict
curl https://raw.githubusercontent.com/ritua2/BOINCatTACC/master/stampede2-backend/S2-test-files/system/controlDict          > system/controlDict
curl https://raw.githubusercontent.com/ritua2/BOINCatTACC/master/stampede2-backend/S2-test-files/system/fvSchemes            > system/fvSchemes
curl https://raw.githubusercontent.com/ritua2/BOINCatTACC/master/stampede2-backend/S2-test-files/system/fvSolution           > system/fvSolution
```





#### **Tutorial for TACC specific applications**  


Note: The script also accounts for job submission using SLURM. In order to utilize BOINC, the job must use 5 or less cores, and below 2048 MB of RAM.




1. AutoDock-Vina  

	* Run *temp-boinc.sh* :

	```bash
	./advance-submit.sh
	```

	* Provide your email when requested

	* Select *1* for *allowed options* when prompted  
	* Select *1* for applications when prompted

	* Continue with the following instructions to run a TACC training file  
		* Provide the following files (space separated):

			```bash
			protein.pdbqt ligand.pdbqt ligand.pdb protein.pdb ligand_experiment.pdb ligand_experiment.pdbqt conf.txt
			```

		* No directories must be provided (enter to skip)
		* Provide the following command (line by line, empty line at the end to exit):

			```bash
			vina --config conf.txt
		```


2. Bedtools  
	* Run *temp-boinc.sh* :

	```bash
	./advance-submit.sh
	```

	* Provide your email when requested

	* Select *1* for *allowed options* when prompted  
	* Select *2* for applications when prompted

	* Continue with the following instructions to run a TACC training file  
		* Provide the following files (space separated):

			```bash
			cpg.bed exons.bed
			```

		* No directories must be provided (enter to skip)
		* Provide the following command (line by line, empty line at the end to exit):

			```bash
			bedtools intersect -a cpg.bed -b exons.bed > bed_test.txt
			```



3. Blast
	* Run *temp-boinc.sh* :

	```bash
	./advance-submit.sh
	```

	* Provide your email when requested

	* Select *1* for *allowed options* when prompted  
	* Select *3* for applications when prompted

	* Continue with the following instructions to run a TACC training file  
		* Provide the following files (space separated):

			```bash
			P04156.fasta zebrafish.1.protein.faa.gz
			```

		* No directories must be provided (enter to skip)
		* Provide the following command (line by line, empty line at the end to exit):

			```bash
			gunzip zebrafish.1.protein.faa.gz
			makeblastdb -in zebrafish.1.protein.faa -dbtype prot
			blastp -query P04156.fasta -db zebrafish.1.protein.faa -out results.txt
			```



4. Bowtie
	* Run *temp-boinc.sh* :

	```bash
	./advance-submit.sh
	```

	* Provide your email when requested

	* Select *1* for *allowed options* when prompted  
	* Select *4* for applications when prompted

	* Continue with the following instructions to run a TACC training file  
		* Provide the following files (space separated):

			```bash
			s_cerevisiae.ebwt.zip
			```

		* No directories must be provided (enter to skip)
		* Provide the following command (line by line, empty line at the end to exit):

			```bash
			unzip s_cerevisiae.ebwt.zip
			bowtie -c s_cerevisiae ATTGTAGTTCGAGTAAGTAATGTGGGTTTG > res_bowtie.txt
			```



5. Gromacs
	* Run *temp-boinc.sh* :

	```bash
	./advance-submit.sh
	```

	* Provide your email when requested

	* Select *1* for *allowed options* when prompted  
	* Select *5* for applications when prompted

	* Continue with the following instructions to run a TACC training file  
		* Provide the following files (space separated):

			```bash
			methane_water.gro topol.top em_steep.mdp
			```

		* No directories must be provided (enter to skip)
		* Provide the following command (line by line, empty line at the end to exit):

			```bash
			gmx grompp -f em_steep.mdp -c methane_water.gro -p topol.top -o min_thing.tpr
			```



6. HTSeq
	* Run *temp-boinc.sh* :

	```bash
	./advance-submit.sh
	```

	* Provide your email when requested

	* Select *1* for *allowed options* when prompted  
	* Select *6* for applications when prompted

	* Continue with the following instructions to run a TACC training file  
		* Provide the following files (space separated):

			```bash
			test.sam gen.gtf
			```

		* No directories must be provided (enter to skip)
		* Provide the following command (line by line, empty line at the end to exit):

			```bash
			htseq-count test.sam gen.gtf > test_htseq.txt
			```



7. MPI-LAMMPS
	* Run *temp-boinc.sh* :

	```bash
	./advance-submit.sh
	```

	* Provide your email when requested

	* Select *1* for *allowed options* when prompted  
	* Select *7* for applications when prompted

	* Continue with the following instructions to run a TACC training file  
		* Provide the following files (space separated):

			```bash
			Al99.eam.alloy aluminium.in
			```

		* No directories must be provided (enter to skip)
		* Provide the following command (line by line, empty line at the end to exit):

			```bash
			mpirun -np 2 lmp_mpi < aluminium.in > lammps_test.txt
			```




8. NAMD
	* Run *temp-boinc.sh* :

	```bash
	./advance-submit.sh
	```

	* Provide your email when requested

	* Select *1* for *allowed options* when prompted  
	* Select *8* for applications when prompted

	* Continue with the following instructions to run a TACC training file  
		* Provide the following files (space separated):

			```bash
			alanin.psf alanin.conf alanin.pdb alanin.params
			```

		* No directories must be provided (enter to skip)
		* Provide the following command (line by line, empty line at the end to exit):

			```bash
			namd2 alanin.conf > results_namd.res
			```


9. OpenSees
	* Run *temp-boinc.sh* :

	```bash
	./advance-submit.sh
	```

	* Provide your email when requested

	* Select *1* for *allowed options* when prompted  
	* Select *9* for applications when prompted

	* Continue with the following instructions to run a TACC training file  
		* Provide the following files (space separated):

			```bash
			MC.tcl
			```

		* No directories must be provided (enter to skip)
		* Provide the following command (line by line, empty line at the end to exit):

			```bash
			OpenSees < MC.tcl
			```


10. CUDA 

	* Run *temp-boinc.sh* :

	```bash
	./advance-submit.sh
	```

	* Provide your email when requested

	* Select *1* for *allowed options* when prompted  
	* Select *10* for applications when prompted

	* Continue with the following instructions to run a TACC training file  
		* Provide the following files (space separated):

			```bash
			happ.cu
			```

		* No directories must be provided (enter to skip)
		* Provide the following command (line by line, empty line at the end to exit):

			```bash
			nvcc happ.cu -o h.out
			./h.out
			```


11. OpenFOAM6 (currently in testing)
	* Run *temp-boinc.sh* :

	```bash
	./advance-submit.sh
	```

	* Provide your email when requested

	* Select *1* for *allowed options* when prompted  
	* Select *11* for applications when prompted

	* Continue with the following instructions to run a TACC training file  
		* No input files are needed:

		* Provide the following directories, each in a new line:
			```bash
			0
			constant
			system
			```
		* Provide the following command (line by line, empty line at the end to exit):

			```bash
			blockMesh
			icoFoam
			```
