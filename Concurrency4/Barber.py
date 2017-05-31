from multiprocessing import Process, Lock
from multiprocessing.managers import BaseManager
from multiprocessing import Manager as man
import random
from time import sleep
import sys


man = man()
mutex = man.Lock()
busyBob = man.Lock()
sharedDict = man.dict()


class Person:
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def getName(self):
        return self.name

    def getRole(self):
        return self.role

    def safeprint(self, toPrint):
        mutex.acquire()
        print(toPrint)
        mutex.release()


class Barber(Person):
    def __init__(self, name, role):
        Person.__init__(self, name, role)
        self.chairsTaken = 0
        self.que = []

    def cutHair(self, customer):
        self.safeprint(self.name + " is cutting " +
                       customer.name + "'s hair \n")
        busyBob.acquire()
        sleep(2)
        busyBob.release()

    def getInLine(self, customer):
        self.safeprint(customer.name + " waives to Bob for a haircut\n")
        self.que.append(customer)
        self.chairsTaken += 1

    def nextCustomer(self):
        curCustomer = self.que.pop(0)
        self.safeprint("Bob says " + curCustomer.name + " you're next! ")
        self.cutHair(curCustomer)

    def barberStart(self):
        self.safeprint(self.getName() + " is going to work.. \n")
        while True:
            if (len(self.que) != 0):
                self.safeprint(self.name + " says 'ok let's get started!'")
                self.nextCustomer()
                self.safeprint(
                    self.name + " just got done cutting hair and is taking a break")
                self.chairsTaken -= 1
                self.printQue()
            else:
                self.safeprint("No one is here.. " +
                               self.name + " is going to sleep")
                self.safeprint(self.name + ": 'zzzzzzz'\n")
            sleep(2)

    def printQue(self):
        tmp = []
        for i in self.que:
            tmp.append(i.name)
        self.safeprint("Current Que for haircuts:")
        self.safeprint(tmp)
        self.safeprint("\n")

    def checkLine(self):
        return self.chairsTaken

    def getque(self):
        return self.que


class Customer(Person):
    def __init__(self, name, role, barber):
        Person.__init__(self, name, role)
        self.barber = barber

    def inque(self):
        inQue = self.barber.getque()
        for i in inQue:
            if i.name == self.name:
                return False
        return True

    def custStart(self):
        while (True):
            self.safeprint(self.getName() +
                           " is about to walk into the barbershop")
            if (self.barber.checkLine() < sharedDict['chairs'] and self.inque()):
                self.safeprint(
                    self.name + " finds a seat to get their hair cut")
                self.barber.getInLine(self)  # get in line
            else:
                self.safeprint(
                    self.name + " can't find a seat and storms out! \n")
            sleep(random.randrange(18, 24) / 1.05)


def buildObjects(barber):
    peopleList = []
    names = ["Abby", "Kelli", "Billy", "Jacob",
             "Poppy", "Brandon", "Sitka", "Sissy"]

    peopleList.append(barber)
    for i in range(0, 8):
        p = Customer(names[i], "Customer", barber)
        peopleList.append(p)
    return peopleList


if __name__ == "__main__":
    try:
        chairs = sys.argv[1]
    except IndexError:
        print("Please put in a number for chairs")
        sys.exit(0)

    BaseManager.register('Barber', Barber)
    manager = BaseManager()
    manager.start()
    # put the Barber class into a manager to be shared
    theBarber = manager.Barber("Bob", "Barber")
    people = buildObjects(theBarber)
    sharedDict['chairs'] = int(chairs)
    print("Chairs used " + str(chairs))
    sharedDict['inLine'] = 0
    for i in people:
        if i.getRole() == "Customer":
            a = Process(target=i.custStart, args=())
        else:
            a = Process(target=i.barberStart, args=())
        sleep(1)
        a.start()
    a.join()
