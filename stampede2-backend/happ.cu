#include "stdio.h"
#define N 10


__global__ void add(int *a, int *b, int *c){
  int tID = blockIdx.x;
  if (tID < N){
    c[tID] = a[tID] + b[tID];
  }
}

int main(){

  int a[N], b[N], c[N];
  int *dev_a, *dev_b, *dev_c;
  cudaMalloc((void **) &dev_a, N*sizeof(int));
  cudaMalloc((void **) &dev_b, N*sizeof(int));
  cudaMalloc((void **) &dev_c, N*sizeof(int));

  // Fill Arrays
  for (int i = 0; i < N; i++){
    a[i] = i,
    b[i] = 1;
  }
  cudaMemcpy(dev_a, a, N*sizeof(int), cudaMemcpyHostToDevice);
  cudaMemcpy(dev_b, b, N*sizeof(int), cudaMemcpyHostToDevice);
  add<<<N,1>>>(dev_a, dev_b, dev_c);
  cudaMemcpy(c, dev_c, N*sizeof(int), cudaMemcpyDeviceToHost);
  
  // Writes the result to the file
  FILE *fp;
  fp = fopen("/root/shared/results/cuda.txt", "w");

  for (int i = 0; i < N; i++){
    fprintf(fp, "%d + %d = %d\n", a[i], b[i], c[i]);
  }
  fclose(fp);  

  return 0;
}

