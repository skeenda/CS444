#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include "mt19937ar.c" //For Mersenne twister
#include <time.h>

struct Data {
    int value;
    int wait;
};

struct Data data_lst[32];
pthread_mutex_t mtx;
pthread_cond_t condition;
int buf_no = 0; // Global variable
int rand_chk;

unsigned int use_rdrand() {
    unsigned int to_return=0;
    __asm__ __volatile__(
                         "rdrand %0;"
                         : "=r"(to_return)
                         );
    return to_return;
}

int check_for_rdrand() {
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

unsigned int get_rand() {
    if(rand_chk)
        return use_rdrand();
    else
        return genrand_int32();
}

struct Data make_data() {
    struct Data data;
    data.value = get_rand() % 50 + 1 ; // 1 - 50
    data.wait = get_rand() % 9 + 2; // between 2-9
    return data;
}

void *producerJob(void *id) {
    int pst = 0;
    struct Data data;

    while(1){
        pst = get_rand() % 5 + 3; // 3-7
        data = make_data();

        if (buf_no <= 32){
          pthread_mutex_lock(&mtx);
          data_lst[buf_no++] = data;

          printf("PRODUCER with id: %d, has produced random # %d, \
                  and the cost for the number was %d, sleeping for \
                  %d seconds \n", (int)id,
        				  data.value,
        				  data.wait,
        				  pst);
          pthread_cond_signal(&condition);
          pthread_mutex_unlock(&mtx);

          printf("PRODUCER with id: %d pushed data on index %d \n \n", (int) id,buf_no-1);
      }else{
        printf("Oh nose! Buffer full! \n \n");
      }
      sleep(pst); // put outside of mutex so it doesn't hang system
    }

    pthread_exit(NULL);
}

void *consumerJob(void *id)
{
    struct Data data;
    while(1){
        if (buf_no >= 1){
          pthread_mutex_lock(&mtx);
          data = data_lst[--buf_no];
          printf("CONSUMER with id: %d, found item w/ value %d \
                  \n Now sleep for %d\n", (int)id,
                  data.value,
                  data.wait);
          printf("CONSUMER with id: %d pulled from index %d\n \n",(int) id, buf_no);
          pthread_cond_signal(&condition);
          pthread_mutex_unlock(&mtx);
      }else{
        printf("Oh nose!! Buffer empty!! \n \n");
        sleep(1);
      }
        sleep(data.wait);
    }
    pthread_exit(NULL);
}

void init_mutex(){
    int mrv = 100;//Mutex Return Value
    int cv = 100;//Conditional calue
    cv = pthread_cond_init(&condition, 0);
    mrv = pthread_mutex_init(&mtx, NULL);

    if (mrv != 0 || cv != 0){
        printf("Error in pthread initization, exiting..");
        exit(1);
    }
}


int main(int argc, char** argv){
     init_mutex();
     pthread_t *producer,*consumer;

     int i = 0; //thread ids
	   int thread_count = 0;

	   if(argc != 2 || atoi(argv[1]) <= 0){
		    printf("Usage: %s <Int>\n", argv[0]);
        printf("Please use a CLI number to give # of threads to use \n");
		    return 1;
	   }

	   thread_count = atoi(argv[1]);
	   printf("Creating %d producer and %d consumer threads\n", thread_count, thread_count);

	   producer = malloc(sizeof(pthread_t) * thread_count);
	   consumer = malloc(sizeof(pthread_t) * thread_count);

     rand_chk = check_for_rdrand();

	   for(i = 0; i < thread_count*2; i += 2){
		     pthread_create(&producer[i], NULL, &producerJob, (void *)i);
		     pthread_create(&consumer[i], NULL, &consumerJob, (void *)i+1);
      }

	    for(i = 0; i < thread_count*2; i += 2){
		      pthread_join(producer[i], NULL);
		      pthread_join(consumer[i], NULL);
	    }

      pthread_mutex_destroy(&mtx);
      pthread_cond_destroy(&condition);
      return 0;
}
