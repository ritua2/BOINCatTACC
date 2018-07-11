#!/bin/bash
PS3="Chose your selection: "

echo "Welcome to job submission script"
echo "We are asking set of interactive questions so that we can judge the best run"
echo -n "What is turnaround time in minute : "
read turnaroundtime
if (( turnaroundtime > 5 && turnaroundtime < 30 ))
then
  server="boinc"
else
  server="stampede"
fi      
echo -n "What is the number of cores required for execution : "
read reqcores
if (( reqcores > 8 ))
then
  server="stampede"
fi
echo -n "How much memory will be required for this job(in MB) : "
read reqmemory
if (( reqmemory > 2048 ))
then
  server="stampede"
fi
echo -n "Please enter your allocation unit : "
read allocation

#select choice in "boinc" "stampede" "quit"
#do
echo "You chose $server"
  case $server in
    boinc)
        echo "Welcome to Boinc job submission:"
        echo "NOTE: No jobs with external communication, large data transfer is expected."
        echo -n "Enter the path of the file which contains list of serial commands : "
        read filetosubmit
        echo "$filetosubmit"
        echo -n "Enter the your user token : "
        read userToken
        echo -n "Enter the boinc server ip address : "
        read SERVER_IP

        curl -F file=@$filetosubmit http://$SERVER_IP:5075/boincserver/v2/submit_known/token=$userToken
        echo "Your request is submitted."
        ;;
    stampede)
        echo "Executing within stampede server"
        echo "How is your command looks"
        echo -n "Please tell us which job queue you would like to use : KNL or SKX : "
        read jobqueue
        #converting jobqueue to lowercase
        jobqueue=${jobqueue,,}
        echo "$jobqueue"
        if [[ $jobqueue != "knl" && $jobqueue != "skx" ]]
        then
            echo $jobqueue
            echo "Wrong queue selection!! Exiting..."
            exit 1
        fi
        select commandtype in "Serial" "MPI" "OpenMP" "Hybrid" "GPU"
        do
          case $commandtype in
            1|serial|Serial)
              cat template_serial.txt > thisrun.txt
              if [ $jobqueue == "skx" ]
              then      
                sed -i 's/for TACC Stampede2 KNL nodes/for TACC Stampede2 SKX nodes/g' thisrun.txt
                sed -i 's/Serial Job on Normal Queue/Serial Job on SKX Normal Queue/g' thisrun.txt
                sed -i 's/sbatch knl.serial.slurm on a Stampede2 login node./sbatch skx.serial.slurm on a Stampede2 login node./g' thisrun.txt
                sed -i 's/SBATCH -p normal/SBATCH -p skx-normal/g' thisrun.txt
              fi        
              break;
            ;;
            2|mpi|MPI)
              cat template_mpi.txt > thisrun.txt
              if [ $jobqueue == "skx" ]
              then
                sed -i 's/for TACC Stampede2 KNL nodes/for TACC Stampede2 SKX nodes/g' thisrun.txt
                sed -i 's/MPI Job on Normal Queue/MPI Job on SKX Normal Queue/g' thisrun.txt
                sed -i 's/sbatch knl.mpi.slurm on Stampede2 login node/sbatch skx.mpi.slurm on Stampede2 login node/g' thisrun.txt
                sed -i 's/Max recommended MPI tasks per KNL node: 64-68/Max recommended MPI ranks per SKX node: 48/g' thisrun.txt
                sed -i 's/SBATCH -p normal/SBATCH -p skx-normal/g' thisrun.txt
              fi
              break;
            ;;
            3|openmp|OpenMP)
              echo "Asking questions related to OpenMP"
              echo -n "Please enter the number of threads you want for parallel execution : "
              read threadcount
              cat template_openmp.txt > thisrun.txt
              if [ $jobqueue=="skx" ]
              then
                sed -i 's/for TACC Stampede2 KNL nodes/for TACC Stampede2 SKX nodes/g' thisrun.txt
                sed -i 's/OpenMP Job on Normal Queue/OpenMP Job on SKX Normal Queue/g' thisrun.txt
                sed -i 's/sbatch knl.openmp.slurm on a Stampede2 login node./sbatch skx.openmp.slurm on a Stampede2 login node./g' thisrun.txt
                sed -i 's/is often 68 (1 thread per core) or 136 (2 threads per core)/is often 48 (1 thread per core) but may be higher/g' thisrun.txt
                sed -i 's/SBATCH -p normal/SBATCH -p skx-normal/g' thisrun.txt
              fi
              break;
            ;;
            4|hybrid|Hybrid)
              echo "Asking questions related to OpenMP"
              echo -n "Please enter the number of threads you want for parallel execution : "
              read threadcount
              cat template_hybrid.txt > thisrun.txt
              if [ $jobqueue=="skx" ]
              then
                sed -i 's/for TACC Stampede2 KNL nodes/for TACC Stampede2 SKX nodes/g' thisrun.txt
                sed -i 's/Hybrid Job on Normal Queue/Hybrid Job on SKX Normal Queue/g' thisrun.txt
                sed -i 's/sbatch knl.hybrid.slurm on Stampede2 login node/sbatch skx.mpi.slurm on Stampede2 login node/g' thisrun.txt
                sed -i 's/SBATCH -p normal/SBATCH -p skx-normal/g' thisrun.txt
              fi
              break;
            ;;
            5|gpu|GPU)
                echo "Not yet supported"
                cat template_gpu.txt >thisrun.txt
              if [ $jobqueue=="skx" ]
              then
                echo "replacement yet to be done"
              fi
              break;
            ;;
            *)
             echo "Wrong selection"     
          esac
        done

        read -p "Do you have some preprocessing task before executing the final task eg. load a module, copying header files? ";
        if [ $REPLY == "y" -o REPLY == "Y" ]; then
          echo -n "Enter the path of preprocessing file which contains preprocessing commands(eg. dependent module load, copying headers): "
          read ppfilepath
          echo "$ppfilepath"
        fi
        echo -n "Enter the path of file which contains the commands to be exectued by stampede server : "
        read commandpath
        commands=$(<$commandpath)
        echo "$commandpath"
        echo "Executing the command $commands"
        #$reading template file
        while IFS='' read -r line || [[ -n "$line" ]]; do
          echo "Text read from file: $line"
        done < thisrun.txt
        #Temp
        cat thisrun.txt > template.txt
        #Actual replacement happening here
        sed -i "s/@allocation_name/$allocation/g" thisrun.txt

        #if threadcount is not null this is openmp or hybrid job.
        if [ -n "$threadcount" ]
        then
          sed -i "s/@threadcount/$threadcount/g" thisrun.txt
        fi
        #if there is any preprocessing file insert that file.
        if [ -n "$ppfilepath" ]
        then
          sed -i -e "s/@preprocessing_commands/$(sed -e 's/[\&/]/\\&/g' -e 's/$/\\n/' $ppfilepath | tr -d '\n')/g" thisrun.txt
        else
          sed -i '/@preprocessing_commands/d' thisrun.txt 
        fi
        sed -i -e "s/@user_commands/$(sed -e 's/[\&/]/\\&/g' -e 's/$/\\n/' $commandpath | tr -d '\n')/g" thisrun.txt 
        #After replacement reading file
        echo "****************************After template replacement**********************************"
        while IFS='' read -r line || [[ -n "$line" ]]; do
          echo "Text read from file: $line"
        done < thisrun.txt
        echo "Do you want to submit this above template to $server? with sbatch cmd"
        read finalsubmission
        if [[ $finalsubmission = "y" || $finalsubmission = "Y" ]]
        then
            #Do the job of sending this file execution.
            sbatch thisrun.txt
        else
            echo "exiting without submission..."
            exit 1;
        fi 
        rm thisrun.txt
        ;;
    quit)
        break
        ;;      
    *)
        echo "You selected a wrong choice"
        ;;
  esac
#done
