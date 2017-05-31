from multiprocessing import Process, Lock
from multiprocessing import Manager as man
import random
from time import sleep

man = man()
sharedDict = man.dict()
listONames = ["Abby", "Poppy", "Brandon", "Kelli", "Billy", "Jacob"]
dictLock, printLock = man.Lock(), man.Lock()


def safePrint(toPrint):
    printLock.acquire()
    print(toPrint)
    printLock.release()


def resetDict():
    sharedDict['name'], sharedDict['count'], sharedDict['free'] = [], 0, True


def f(name):
    while True:
        if (sharedDict['count'] < 3 and sharedDict['free'] == True):
            sharedDict['count'] += 1
            safePrint(name + " got access!")
            if (sharedDict['count'] == 3):
                sharedDict['free'] = False
                safePrint("-------WE HAVE HIT 3 PEOPLE---------")
            tmp = sharedDict['name']
            tmp.append(name)
            sharedDict['name'] = tmp
            safePrint(sharedDict._getvalue()['name'])
            sleep(5)
            tmp = sharedDict['name']
            tmp.remove(name)
            sharedDict['name'] = tmp
            sharedDict['count'] = sharedDict['count'] - 1
            safePrint(name + " DONE!!")
            if (sharedDict['count'] == 0):
                resetDict()
                safePrint(
                    name + " was last one out! Now it's free again!" + "\n")
            safePrint(sharedDict._getvalue())
            sleep(random.randrange(5, 10))
        else:
            safePrint(
                name + " says 'Oh nose, I been blocked, I guess I will sleep!'")
            safePrint(name + " says 'These people are hogging it all'")
            safePrint(sharedDict._getvalue())

            print("\n")
        sleep(random.randrange(5, 15) / 1.25)


if __name__ == "__main__":
    resetDict()
    for i in range(0, 6):
        p = Process(target=f, args=(listONames[i],))
        sleep(1)
        p.start()
    p.join()
