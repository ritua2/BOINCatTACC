#run this script from the directory that contains tar files that need to be extracted
#!/bin/bash
for a in `ls -1`
 do 
        cd $a; 
        ls -1 *.tar | xargs -n1 tar -xf; 
        for b in `ls -1d */`
        do
           cd $b;
           ls -1 *tar.gz | xargs -n1 tar -xzf;
           cd ..;
        done
        cd .. ;
 done
