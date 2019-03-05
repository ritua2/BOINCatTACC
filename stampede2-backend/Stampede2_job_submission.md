### Job submission through Stampede2
-------


* **Prerequisites**  
Instructions below require access to the TACC Stampede2 supercomputer  



* **Installation**  
Obtain the required files from [this directory](./S2-test-files):


```bash
ml git
git clone https://github.com/ritua2/BOINCatTACC
cd BOINCatTACC/stampede2-backend/S2-test-files
chmod +x advance-submit.sh
```


* **Tutorial for TACC specific applications**  


Note: The script also accounts for job submission using SLURM. In order to utilize BOINC, the job must use 8 or less cores, and below 2048 MB of RAM.




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



7. Bowtie
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


10. OpenFOAM6
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
