#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <omp.h>
int main(int argc, char *argv[]){
if(argc < 3){
 printf("Missing argument: please provide a script name or command that should be run on multiple cores. For example: ./prepare_directories_parallel test_PDBQT.txt 5r80.pdbqt\n");
 exit (-1);
}else{
  char command[1000];
  char argv1[100], argv2[100];
  strcpy(argv2, argv[2]);
  strcpy(argv1, argv[1]);
  sprintf(command, "./step_1.sh %s %s", argv[1], argv[2]);
  system(command);
  int i, start, end;
  char filename[100];
  FILE *fp = fopen("read_from.txt", "r");
  if (fp!=NULL){
        fscanf(fp,"%d", &start);
        fscanf(fp,"%d", &end);
        fscanf(fp,"%s", &filename);

  }
  #pragma omp parallel for default(none) shared(start, end, argv1, argv2) private (i, command) 
  for(i=start; i<=end; i++){
        printf("\nthread id is: %d, i is : %d, argv1: %s, argv2: %s\n", omp_get_thread_num(), i, argv1, argv2);
        sprintf(command, "./step_2.sh %d %s %s", i,argv1, argv2);
        system(command);
  }

  fclose(fp);
}
return 0;
}
