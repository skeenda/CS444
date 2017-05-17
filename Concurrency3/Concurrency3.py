from multiprocessing import Process, RLock, Array
from multiprocessing import Manager as man
import random
from time import sleep

searcherLock, inserterLock, deleterLock = RLock(), RLock(), RLock()
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
        sleep(1.75)
        if(isNotLocked(searcherLock)):
            searcherLock.acquire(False)
            try:
                searcherLock.release()
            except AssertionError:
                pass
            else:
                pass
            # Searcher doesnt need to actually lock searcher lock,
            # Just needs to make sure its not locked by deleter thread
            # look through list
            print(str(id))
            print(str(id) + " SEARCHING: " + str(sharedList))
            print(str(id) + " DONE SEARCHING!!! \n")
        else:
            print(str(id) + " HAS BEEN BLOCKED!!! \n")


def inserter(id):

    while (True):
        sleep(1.5)
        if (isNotLocked(deleterLock)
                and isNotLocked(inserterLock)):
            deleterLock.acquire(False)
            inserterLock.acquire(False)
            print(str(
                id) + " has deleteLock and insertLock, blocking other delters and inserters!! \n")
            randNum = random.randint(1, 20)
            appendData = id + str(" has appended ") + str(randNum)
            print(str(appendData))
            sharedList.append(randNum)
            print(id + " " + str(sharedList) + " DONE!!! \n")
            try:
                deleterLock.release()
                inserterLock.release()
            except AssertionError:
                pass
            else:
                pass
        else:
            print(str(id) + " HAS BEEN BLOCKED!!! \n")

            # Block out:
            #   other inserters
            #   any deleters
            # Critical part


def deleter(id):
    while(True):
        sleep(1)
        if (isNotLocked(deleterLock) and isNotLocked(inserterLock) and isNotLocked(searcherLock)):
            deleterLock.acquire(False)
            inserterLock.acquire(False)
            searcherLock.acquire(False)
            if (len(sharedList) > 0):
                removed = sharedList.pop()
                print(str(id) + " has deleted " + str(removed))
                print(id + " " + str(sharedList) + " DONE!! \n")
            try:
                deleterLock.release()
                inserterLock.release()
                searcherLock.release()
            except AssertionError:
                pass
            else:
                pass
        else:
            print(str(id) + " BLOCKED!!! \n")

    # Block out
    #   inserters
    #   Deleters
    #   Searchers


def isNotLocked(lock):
    if (lock.acquire(False)):
        lock.release()
        return True
    else:
        return False


def startStuff():
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
    startStuff()
