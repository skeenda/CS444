from multiprocessing import Process, Lock
from multiprocessing import Manager as man
import random
from time import sleep

man = man()
searcherLock, inserterLock, deleterLock = man.Lock(), man.Lock(), man.Lock()
names = man.Namespace()
names.searchLock, names.insertLock, names.deleteLock = "None", "None", "None"
sharedList = man.list()


def findBlockers(id):
    print(str(id) + " BLOCKED!!! " + str(names) + " \n")
    sleep(random.randint(2, 8))


def searcher(id):
    while(True):
        if not ("deleter:" in names.deleteLock):
            print(str(id) + " Starting search: " + str(names))
            sleep(1.75)
            print(id + " FOUND " + str(sharedList))
            print(str(id) + " DONE SEARCHING!!! \n")
            sleep(random.randrange(2, 15, 1) / 1.25)

        else:
            findBlockers(id)


def inserter(id):
    while (True):
        if (isNotLocked(deleterLock, inserterLock)):
            names.deleteLock, names.insertLock = id, id
            print("STARTING: " + id + str(names))
            randNum = random.randint(1, 20)
            sleep(1.75)
            appendData = id + str(" has appended ") + str(randNum)
            print(str(appendData))
            sharedList.append(randNum)
            deleterLock.release()
            inserterLock.release()
            names.deleteLock, names.insertLock = "None", "None"
            print(id + " " + str(sharedList) + " DONE!!! " + str(names) + "\n")
            sleep(random.randrange(2, 15, 1) / 1.25)
        else:
            findBlockers(id)


def deleter(id):
    while(True):
        if (isNotLocked(deleterLock, inserterLock, searcherLock)):
            names.deleteLock, names.insertLock, names.searchLock = id, id, id
            print("STARTING: " + id + " " + str(names))
            sleep(1.75)
            if (len(sharedList) > 0):
                removed = sharedList.pop()
                print(str(id) + " has deleted " + str(removed))
                print(id + " has made list " + str(sharedList) + "\n")
            deleterLock.release()
            inserterLock.release()
            searcherLock.release()
            names.deleteLock, names.insertLock, names.searchLock = "None", "None", "None"
            print(str(id) + " DONE!!! " + str(names))
            sleep(random.randrange(2, 15, 1) / 1.25)
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
