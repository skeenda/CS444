import multiprocessing as mt
import random
import time
'''
Authors: Brandon Dring, William Buffman, Samuel Jacobs

Script to solve dining philosophers problem
'''
forks, jobs, philosophers = [], [], [
    "Plato", "Aristotle", "Karl Marx", "Confuscious", "Socrates"]

philopid = {"Plato": "-1", "Aristotle": "-2",
            "Karl Marx": "-3", "Confuscious": "-4", "Socrates": "-5"}


def think(num):
    thinkTime = random.randint(1, 20)
    print(str(num) + ", thinking for " + str(thinkTime) + " seconds\n")
    time.sleep(thinkTime)


# Include thread who is trying to access resource
def eat(num, leftFork, rightFork):
    eatTime = random.randint(2, 9)
    print(str(num) + ",  eating for " + str(eatTime) + " seconds")
    print("with forks ", leftFork, rightFork)
    print("\n")
    time.sleep(eatTime)


def get_forks(num, leftFork, rightFork, test, test2):
    if test is True and test2 is True:
        leftPid = str(leftFork['available'])[19:-2]
        rightPid = str(rightFork['available'])[19:-2]
        if (philopid[num] == leftPid and philopid[num] == rightPid):
            print(num + " says \"Yum, I can eat\"")
            eat(num, leftFork, rightFork)
            print(num + " kindly puts down", leftFork, rightFork)

    else:
        print(num + " is missing a fork")
        print(leftFork, rightFork)
        return


def put_forks(num, leftFork, rightFork):
    rightFork['available'].release()
    leftFork['available'].release()


def philosopher(num, idx):
    leftFork, rightFork = forks[idx], forks[(idx + 1) % 5]
    if leftFork['id'] > rightFork['id']:  # Swap forks for last philosopher to prevent deadlock
        rightFork, leftFork = leftFork, rightFork

    print(num + " can use ", leftFork, rightFork)
    while True:
        print(num, idx)
        test = leftFork['available'].acquire()
        test2 = rightFork['available'].acquire()
        print("\n")
        think(num)
        get_forks(num, leftFork, rightFork, test, test2)
        put_forks(num, leftFork, rightFork)


def buildForks():
    for i in range(0, 5):
        lock = mt.Lock()
        fork = {
            'id': i,
            'available': lock  # Mutex instead of True/False
        }
        forks.append(fork)
    return forks


if __name__ == "__main__":
    buildForks()
    for i in range(0, 5):
        p = mt.Process(
            target=philosopher, args=(philosophers[i], i,))
        p.start()
