from multiprocessing import Process, Lock
from multiprocessing import Manager as man
import random
from time import sleep
import sys

man = man()
printLock = man.Lock()
tableLock = man.Lock()
onTable = man.list()


class Person:
	def __init__(self, name, role):
		self.name = name
		self.role = role
		print('Hi my name is ' + name)

	def safePrint(self, toPrint):
		printLock.acquire()
		print(toPrint)
		printLock.release()


class smoker(Person):
	def __init__(self, name, has, role):
		Person.__init__(self, name, role)
		self.has = has
		self.needs = self.getNeeds(self.has)
		print("I need", self.needs)

	def getNeeds(self, has):
		needs = []
		products = ["tobacco", "paper", "matches"]
		for i in products:
			if (str(has) != str(i)):
				needs.append(i)
		return needs

	def smokerStart(self):
		print("SMOKER waiting")
        while(True):
            sleep(2)
            print(self.name + " needs to smoke")




class agent(Person):
	def __init__(self, name, role):
		Person.__init__(self, name, role)

	def giveOut(self, ingredient1, ingredient2):
		pass

	def agentStart(self):
		print("AGENT waiting..")


def buildPeople():
	l = []
	l.append(agent("Craig", "agent"))
	l.append(smoker("Bob", "paper", "smoker"))
	l.append(smoker("Tom", "tobacco", "smoker"))
	l.append(smoker("John", "matches", "smoker"))
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





