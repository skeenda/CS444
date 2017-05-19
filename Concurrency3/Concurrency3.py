from multiprocessing import Process, Lock
from multiprocessing import Manager as man
import random
from time import sleep

man = man()
searcherLock, inserterLock, deleterLock = man.Lock(), man.Lock(), man.Lock()
names = man.Namespace()
names.searchLock, names.insertLock, names.deleteLock = "None", "None", "None"
sharedList = man.list()

"""
searchers: parallel with searchers
inserters: block inserters, parallel with searchers
deleters: block deleters, block inserters, block searchers
"""


def findBlockers(id):
    print(str(id) + " BLOCKED!!!" + str(names) + " \n")
    sleep(random.randint(2, 5))


def searcher(id):
    while(True):
        if not ("deleter:" in names.deleteLock):
            names.deleteLock = str(id)
            print(str(id) + " Starting search: " + str(sharedList))
            sleep(1)
            print(str(id) + " DONE SEARCHING!!! \n")
            print(id + " FOUND " + str(sharedList) + str(names))
            names.deleteLock = "None"
            sleep(random.randint(2, 5))
        else:
            findBlockers(id)


def inserter(id):
    while (True):
        if (isNotLocked(deleterLock, inserterLock)):
            names.deleteLock = id
            names.insertLock = id
            print("STARTING: " + id)
            randNum = random.randint(1, 20)
            sleep(1)
            appendData = id + str(" has appended ") + str(randNum)
            print(str(appendData))
            sharedList.append(randNum)
            deleterLock.release()
            inserterLock.release()
            print(id + " " + str(sharedList) + " DONE!!! " + str(names) + "\n")
            names.deleteLock = "None"
            names.insertLock = "None"
            sleep(random.randint(2, 5))
        else:
            findBlockers(id)


def deleter(id):
    while(True):
        if (isNotLocked(deleterLock, inserterLock, searcherLock)):

            names.deleteLock = id
            names.insertLock = id
            names.searchLock = id
            print("STARTING: " + id)
            sleep(1)
            if (len(sharedList) > 0):
                removed = sharedList.pop()
                print(str(id) + " has deleted " + str(removed))
                print(id + " has made list " + str(sharedList) + "\n")
            deleterLock.release()
            inserterLock.release()
            searcherLock.release()
            print(str(id) + " DONE!!! " + str(names))
            names.deleteLock = "None"
            names.insertLock = "None"
            names.searchLock = "None"

            sleep(random.randint(2, 5))
        else:
            findBlockers(id)


def isNotLocked(*lock):
    todo = []
    for i in lock:
        if i.acquire(False):
            todo.append(i)
        else:
            for j in todo:
                j.release()
            return False
    return True


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
