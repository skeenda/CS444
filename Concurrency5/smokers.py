from multiprocessing import Process, Lock
from multiprocessing import Manager as man
import random
from time import sleep
import collections

man = man()
onTable = man.list()
printLock = man.Lock()
tableLock = man.Lock()


class Person:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.products = ["tobacco", "paper", "matches"]
        print('Hi my name is ' + name)

    def safeprint(self, toPrint):
        printLock.acquire()
        print(toPrint)
        printLock.release()


class smoker(Person):
    def __init__(self, name, has, role, agent):
        Person.__init__(self, name, role)
        self.has = has
        self.needs = self.getNeeds(self.has)
        self.safeprint("I need" + str(self.needs))
        self.onTable = []
        self.agent = agent

    def getTable(self):
        self.onTable = onTable

    def getNeeds(self, has):
        needs = []
        for i in self.products:
            if (str(has) != str(i)):
                needs.append(i)
        return needs

    def checkTable(self):
        tableLock.acquire()
        self.getTable()
        print(self.name + " needs " + str(self.needs) +
              " and there is only" + str(self.onTable) + " on the table")
        if set(self.needs) == set(self.onTable):
            self.safeprint(
                self.name + " FOUND what he needs to make a cigarette and says 'ah that's good!' \n")
            self.agent.clearList()
        else:
            self.safeprint(
                self.name + " says 'there is no god damn cigarettes!' \n")
        tableLock.release()

    def smokerStart(self):
        while (True):
            sleep(3)
            self.safeprint(self.name + " needs to smoke")
            self.checkTable()


class agent(Person):
    def __init__(self, name, role):
        Person.__init__(self, name, role)

    def giveOut(self):
        for n in random.sample(range(0, 3), 2):
            onTable.append(self.products[int(n)])

    def clearList(self):
        onTable[:] = []

    def agentStart(self):
        self.safeprint("AGENT started.. \n")
        while (True):
            self.safeprint("Craig is about to give out some ingredients")
            self.giveOut()
            self.safeprint("Craig put " + str(onTable) + " on the table! \n")
            sleep(4)
            onTable[:] = []


def buildPeople():
    l = []
    p = agent("Craig", "agent")
    l.append(p)
    l.append(smoker("Bob", "paper", "smoker", p))
    l.append(smoker("Tom", "tobacco", "smoker", p))
    l.append(smoker("John", "matches", "smoker", p))
    return l


if (__name__ == "__main__"):
    workersList = buildPeople()
    for i in workersList:
        if i.role == "agent":
            a = Process(target=i.agentStart, args=())
        else:
            a = Process(target=i.smokerStart, args=())
        sleep(1)
        a.start()
    a.join()
