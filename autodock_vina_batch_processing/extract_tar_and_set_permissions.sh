#!/bin/bash
for a in IA  IB  JA  JB
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
        find $a \( -type d -exec chmod g+rx {} \; \) -o \( -type f -exec chmod g+r {} \; \)
 done
