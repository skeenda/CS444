from multiprocessing import Process, Lock
from multiprocessing import Manager as man
import random
from time import sleep

man = man()
printLock = man.Lock()
tableLock = man.Lock()
onTable = man.list()


class Person(object):
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
	def __init__(self, name, has, role):
		Person.__init__(self, name, role)
		self.has = has
		self.needs = self.getNeeds(self.has)
		self.safeprint("I need" + str(self.needs))

	def getNeeds(self, has):
		needs = []
		for i in self.products:
			if (str(has) != str(i)):
				needs.append(i)
		return needs

	def checkTable(self):
		global onTable
		tableLock.acquire()
		if self.needs == onTable:
			self.safeprint(self.name + " found what he needs to make a cigarette and says 'ah that's good!'")
			onTable = []
		else:
			self.safeprint(self.name + " says 'there is no god damn cigarettes!'")
		tableLock.release()

	def smokerStart(self):
		self.safeprint("SMOKER waiting")
		while (True):
			sleep(2)
			self.safeprint(self.name + " needs to smoke")
			self.checkTable()


class agent(Person):
	def __init__(self, name, role):
		Person.__init__(self, name, role)

	def giveOut(self):
		for n in random.sample(range(0, 3), 2):
			onTable.append(self.products[int(n)])
		self.safeprint(str(onTable))

	def agentStart(self):
		self.safeprint("AGENT started..")
		while (True):
			sleep(2)
			self.safeprint("Craig is about to give out some ingredients")
			self.giveOut()
			self.safeprint("Craig put ingredients on the table!")
			sleep(2)


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


