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
