### Job submission through Stampede2
-------


* **Prerequisites**  
Instructions below require access to the TACC Stampede2 supercomputer  



* **Installation**  
Obtain the required files from [this directory](./S2-test-files):


```bash
git clone https://github.com/ritua2/BOINCatTACC
cd BOINCatTACC/stampede2-backend/S2-test-files
chmod +X temp-boinc.sh
```


* **Tutorial for TACC specific applications**  

1. AutoDock-Vina  

	* Run *temp-boinc.sh* :

	```bash
	./temp-boinc.sh
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
	./temp-boinc.sh
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
	./temp-boinc.sh
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


