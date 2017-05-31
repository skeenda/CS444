from multiprocessing import Process, Lock
from multiprocessing import Manager as man
import random
from time import sleep
import sys


man = man()
mutex = man.Lock()
customerL, barberL, customerDone, barberDone = man.Lock(
), man.Lock(), man.Lock(), man.Lock()

sharedDict = man.dict()


class Person:
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def getName(self):
        return self.name

    def getRole(self):
        return self.role

    def ready(self):
        pass


class Barber(Person):
    def __init__(self, name, role):
        Person.__init__(self, name, role)
        self.chairsTaken = 0
        self.wakeUp = False
        self.que = []

    def cutHair(self, customer):
        print(self.name + " is cutting " + customer + " hair")

    def wakeUpBarber(self, customer):
        print(customer.name + " kicks Bob to wake up")
        self.wakeUp = True
        self.que.append(customer)

    def barberStart(self):
        print(self.getName() + " is going to work..")

        # Barber is always cutting hair
        while True:
            print("No one is here.. " + self.name + " is going to sleep")
            while (self.wakeUp == False):
                print(self.name + ": 'zzzzzzz'")
                if (self.wakeUp == True):
                    print(self.name + " says 'ok let's get started'")
                sleep(3)

            # Wait for customer
            customerL.acquire(True)
            # release barber lock
            if barberL.acquire(False):
                barberL.release()
            # cut hair
            # self.cutHair()
            customerDone.acquire(True)
            # barberDone.release()

            customerL.release()


class Customer(Person):
    def __init__(self, name, role, barber):
        Person.__init__(self, name, role)
        self.barber = barber

    def getHairCut(self, barber):
        print(self.name + " is getting hair cut by " + barber)

    def custStart(self):
        print("Starting " + self.getName() + "..")

        while (True):
            print(self.getName() + " is about to walk into the barbershop")

            # customer wants to walk into the barbershop but must wait for access
            # mutex.acquire(True)
            self.barber.wakeUpBarber(self)
            sleep(10)
            # customer walks in
            if customers == n:
                # if there are n customers in line, new customer leaves
                # mutex.release()
                print(
                    custName + " balks and walks out of the barbershop because the line is too long")
                sleep(5)
            else:

                # otherwise, customer waits in line
                customers = customers + 1
                mutex.release()

                # customerL.release()

                print(custName + " is waiting in line for a haircut")
                # wait in line for barber
                barberL.acquire(True)

                # get the haircut
                print(custName + " is getting a haircut")

                # done getting haircut
                # customerDone.release()

                # release the barber
                # barberDone.release()

                # leave the barbershop
                #customers = customers - 1


"""
def cutHair(barbName):
    print("Barber " + barbName + " is cutting hair")






"""


def buildObjects():
    peopleList = []

    barber = Barber("Bob", "Barber")
    peopleList.append(barber)
    abby = Customer("Abby", "Customer", barber)
    peopleList.append(abby)
    kelli = Customer("Kelli", "Customer", barber)
    peopleList.append(kelli)
    billy = Customer("Billy", "Customer", barber)
    peopleList.append(billy)
    jacob = Customer("Jacob", "Customer", barber)
    peopleList.append(jacob)
    poppy = Customer("Poppy", "Customer", barber)
    peopleList.append(poppy)
    brandon = Customer("Brandon", "Customer", barber)
    peopleList.append(brandon)
    sitka = Customer("Sitka", "Customer", barber)
    peopleList.append(sitka)
    sissy = Customer("Sissy", "Customer", barber)
    peopleList.append(sissy)
    return peopleList


if __name__ == "__main__":
    """try:
        chairs = sys.argv[1]
    except IndexError:
        print("Please put in a number for chairs")
        sys.exit(0)
        """

    people = buildObjects()
    sharedDict['chairs'] = 4
    sharedDict['inLine'] = 0
    for i in people:
        if i.getRole() == "Customer":
            a = Process(target=i.custStart, args=())
        else:
            a = Process(target=i.barberStart, args=())
        sleep(1)
        a.start()

    a.join()

    """
    b = Process(target=barber, args=('Bob',))
    c1 = Process(target=customer, args=('Abby', chairs,))
    c2 = Process(target=customer, args=('Kelli', chairs,))
    c3 = Process(target=customer, args=('Billy', chairs,))
    c4 = Process(target=customer, args=('Jacob', chairs,))
    c5 = Process(target=customer, args=('Poppy', chairs,))
    c6 = Process(target=customer, args=('Brandon', chairs,))
    c7 = Process(target=customer, args=('Sitka', chairs,))
    c8 = Process(target=customer, args=('Sissy', chairs,))

    b.start()
    c1.start()
    c2.start()
    c3.start()
    c4.start()
    c5.start()
    c6.start()
    c7.start()
    c8.start()
    b.join()
    """
