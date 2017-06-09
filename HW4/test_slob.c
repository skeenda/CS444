#include <stdio.h>
#include <stdlib.h>
#include <sys/syscall.h>
int main(){
	srand(time(NULL));

	int i = 0;
	int** p = (int**)malloc(sizeof(int*)*500);
	int val = 0;
	int rc =0;

	for(i=0;i<500;i++){
		val = rand()%100+50;
		p[i] = (int*)malloc(sizeof(int)*val);
	}
	
	for(i=0;i<500;i++){
		free(p[i]);
		val = rand()%200+100;
		p[i] = (int*)malloc(sizeof(int)*val);
	}
	rc = syscall(353);
	rc = syscall(354);
	for(i=0;i<500;i++){
		free(p[i]);
	}
	free(p);
	return 0;
}
