from multiprocessing import Process, Lock, Array
from multiprocessing import Manager as man
import random
from time import sleep

searcherLock = Lock()
inserterLock = Lock()
deleterLock = Lock()
manager = man()
sharedList = manager.list()
"""

searchers: parallel with searchers
inserters: block inserters, parallel with searchers
deleters: block deleters, block inserters, block searchers

"""


def searcher(id):
    # Block out:
    #   nothing

    while(True):
        print(str(id))
        sleep(2)
        if(isLocked(searcherLock)):
            searcherLock.acquire(False)
            searcherLock.release()
            # Searcher doesnt need to actually lock searcher lock,
            # Just needs to make sure its not locked by deleter thread
            # look through list
            # print("List: ")
            print("TEST: " + str(sharedList))


def inserter(id):

    while (True):
        print("Inserter")

        sleep(2)
        if (isLocked(deleterLock)
                and isLocked(inserterLock)):
            deleterLock.acquire(False)
            inserterLock.acquire(False)
            print(str(id) + "has blocked deleters and other inserters")
            randNum = random.randint(1, 20)
            appendData = id + str(" has appended ") + str(randNum)
            print(appendData)
            sharedList.append(randNum)
            deleterLock.release()
            inserterLock.release()

            # Block out:
            #   other inserters
            #   any deleters
            # Critical part


def deleter(id):
    while(True):
        print(str(id))
        sleep(2)
        if (isLocked(deleterLock) and isLocked(inserterLock) and isLocked(searcherLock)):
            deleterLock.acquire(False)
            inserterLock.acquire(False)
            searcherLock.acquire(False)
            if (len(sharedList) > 0):
                sharedList.pop()
            deleterLock.release()
            inserterLock.release()
            searcherLock.release()

    # Block out
    #   inserters
    #   Deleters
    #   Searchers


def isLocked(lock):
    if (lock.acquire(False)):
        lock.release()
        return True
    else:
        return False


def buildGuys():
    searcherT, inserterT, deleterT = [[] for i in range(0, 3)]
    for i in range(0, 2):
        inserterT.append(Process(
            target=inserter, args=("inserter: " + str(i + 1),)))
        inserterT[i].start()
        searcherT.append(Process(
            target=searcher, args=("searcher: " + str(i + 1), )))
        searcherT[i].start()
        deleterT.append(Process(
            target=deleter, args=("deleter: " + str(i + 1),)))
        deleterT[i].start()
    deleterT[0].join()


if __name__ == "__main__":
    buildGuys()
