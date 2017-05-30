from multiprocessing import Process, Lock
from multiprocessing import Manager as man
import random
from time import sleep

man = man()
sharedLock = man.Lock()
names = man.Namespace()
sharedList = man.dict()


def f(name):
    if (sharedLock.acquire(False) is True):
        print("Took lock first!")

        print(sharedLock)
    print(name)
    sleep(20)
    sharedLock.release()


def g(name):
    print("Attempting to steal lock")
    sharedLock.release()
    if (sharedLock.acquire(False) == True):
        sharedLock.acquire(False)
        print(sharedLock)
        print("I got the lock!")


if __name__ == "__main__":
    sharedList.append([sharedLock, 0])
    p = Process(target=f, args=('Abby',))
    q = Process(target=g, args=('Poppy'))
    p.start()
    q.start()
    p.join()
