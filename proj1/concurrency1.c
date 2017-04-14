#include <stdio.h>
#include <pthread.h>
#include "mt19937ar.c" //For Mersenne twister

struct Data {
  int value;
  int waitTime;
};

struct Data dataList[32];
pthread_mutex_t myMutex;
int bufferNumber = 0; // Global variable

/*
  TODO
    - Implement rdrand option for random number gen
    - change sleep to a mutex condition
*/


void *producerJob(void *id){
  int idx = 0;
  int producerSleepTime = 0;
  int randNumber = -1;
  int dataSleepTime = -1;
  struct Data data;

  while(1){
    printf("Thread %d doing work ", id);
    producerSleepTime = genrand_int32() % 5 + 3; // 3-7
    randNumber = genrand_int32() % 50 + 1 ; // 1 - 50
    dataSleepTime = genrand_int32() % 9 + 2; // between 2-9

    printf("This is the sleep time %d \n", producerSleepTime);
    sleep(producerSleepTime);
    data.value = randNumber;
    data.waitTime = dataSleepTime;

    while (bufferNumber >= 32)
      sleep(0.2);

    pthread_mutex_lock(&myMutex);
    dataList[idx] = data;
    printf("Producer has produced random # %d, and the cost for the number was %d, sleeping for %d seconds \n",randNumber, dataSleepTime, producerSleepTime);
    bufferNumber += 1;
    pthread_mutex_unlock(&myMutex);
    idx++;
    printf("On index %d \n",idx);
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
  pthread_t producer;
  int i = 0;
  pthread_create(&producer, NULL, &producerJob,NULL);
  printf("I'm here!\n");

  pthread_exit(NULL);

  pthread_mutex_destroy(&myMutex);
  return 0;
}
