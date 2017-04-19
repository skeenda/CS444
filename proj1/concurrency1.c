#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include "mt19937ar.c" //For Mersenne twister
#include <time.h>

struct Data {
    int value;
    int waitTime;
};

struct Data dataList[32];
pthread_mutex_t myMutex;
pthread_cond_t condition;
int bufferNumber = 0; // Global variable
int rand_chk;

unsigned int use_rdrand()
{
    unsigned int to_return=0;
    __asm__ __volatile__(
                         "rdrand %0;"
                         : "=r"(to_return)
                         );
    return to_return;
}

int check_for_rdrand()
{

    unsigned int eax;
    unsigned int ebx;
    unsigned int ecx;
    unsigned int edx;

    char vendor[13];
    
    eax = 0x01;

    __asm__ __volatile__(
                         "cpuid;"
                         : "=a"(eax), "=b"(ebx), "=c"(ecx), "=d"(edx)
                         : "a"(eax)
                         );
    
    if(ecx & 0x40000000)
        return 1;
    else
        return 0;
}

unsigned int get_rand()
{
    if(rand_chk)
        return use_rdrand();
    else
        return genrand_int32();
}

void *producerJob(void *id)
{
    int producerSleepTime = 0;
    struct Data data;

    while(1){
        printf("Thread %d doing work \n", id);
        producerSleepTime = get_rand() % 5 + 3; // 3-7
        data.value = get_rand() % 50 + 1 ; // 1 - 50
        data.waitTime = get_rand() % 9 + 2; // between 2-9

        while (bufferNumber >= 32)
            sleep(0.2);

        sleep(producerSleepTime); // put outside of mutex so it doesn't hang system

        pthread_mutex_lock(&myMutex);
        dataList[bufferNumber] = data;
        printf("Producer has produced random # %d, and the cost for the number was %d, sleeping for %d seconds \n",data.value, data.waitTime, producerSleepTime);
        bufferNumber++;
        pthread_cond_signal(&condition);
        pthread_mutex_unlock(&myMutex);

        printf("On index %d \n",bufferNumber-1);
        //NB: slightly changed this
        // bufferNumber is number of items in buffer,
        // not index
        // well I guess its technically the index 
        // of where the NEXT item WILL be placed
    }

    pthread_exit(NULL);
}

void *consumerJob(void *id)
{
    struct Data data;
    while(1){
        printf("Consumer Thread %d doing work \n", (int)id);
        while(bufferNumber <= 0){
            //printf("COnsumer thinks bufferNumber is %d\n",bufferNumber);
        }
        pthread_mutex_lock(&myMutex);
        data = dataList[--bufferNumber];
        //bufferNumber--;
        printf("Consumer %d found item w/ value %d \
                \n Now sleep for %d\n", (int)id, 
                data.value,
                data.waitTime);
        pthread_cond_signal(&condition);
        pthread_mutex_unlock(&myMutex);

        sleep(data.waitTime);
    }
    pthread_exit(NULL);
}

void initMutex(){
    int mutexReturnVal = 100;
    int condVal = 100;
    condVal = pthread_cond_init(&condition, 0);
    mutexReturnVal = pthread_mutex_init(&myMutex, NULL);

    if (mutexReturnVal != 0 || condVal != 0){
        printf("Error in pthread initization, exiting..");
        exit(1);
    }
}


int main(){
    initMutex();
    pthread_t producer, consumer;
    int i=0;
    rand_chk = check_for_rdrand();
    pthread_create(&producer, NULL, &producerJob,(void*)i++);
    pthread_create(&consumer, NULL, &consumerJob,(void*)i);

    printf("I'm here!\n");

    pthread_join(producer,NULL);
    pthread_join(consumer,NULL);

    pthread_mutex_destroy(&myMutex);
    pthread_cond_destroy(&condition);
  return 0;
}
