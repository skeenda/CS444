#include <stdio.h>
#include <pthread.h>
#include "mt19937ar.c" //For Mersenne twister

struct Data {
  int value;
  int waitTime;
};
struct Data dataList[32];

pthread_mutex_t myMutex;

/*
  TODO
    - Implement rdrand option for random number gen
*/


void *producerJob(void *id){
  int idx = 0;
  int producerSleepTime = 0;
  int randNumber = -1;
  int dataSleepTime = -1;
  struct Data data;

  while(idx < 100){
    printf("Thread %d doing work ", id);
    producerSleepTime = genrand_int32() % 5 + 3;
    randNumber = genrand_int32() % 50 + 1 ; // 1 - 50
    dataSleepTime = genrand_int32() % 9 + 2; // between 2-9

    printf("This is the sleep time %d \n", producerSleepTime);
    sleep(producerSleepTime);


    printf("Rand number generated %d \n", randNumber);
    printf("data generated sleep time %d \n \n", dataSleepTime);
    idx++;
  }
  pthread_exit(NULL);
}

void initMutex(){
  int mutexReturnVal = 100;
  mutexReturnVal = pthread_mutex_init(&myMutex, NULL);
  if (mutexReturnVal != 0){
    printf("Mutex could not be initialized, exiting..");
    exit(1);
  }
}


int main(){
  initMutex();
  pthread_t thread[5];
  int i = 0;
  for (i = 0; i < 5; i++){
    int returnVal =0;
    returnVal= pthread_create(&thread[i], NULL, &producerJob, (void *)i);
  }
  printf("I'm here!\n");

  pthread_exit(NULL);

  pthread_mutex_destroy(&myMutex);
  return 0;
}
