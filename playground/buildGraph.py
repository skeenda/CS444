import numpy as np
import matplotlib.pyplot as plt
import sys


def doWork(file):
    fo = open(file, "r+")
    data = fo.read().split("\n")
    points, idx, num = [], [], 0
    plt.figure()
    for i in data:
        num += 1
        idx.append(num)

        clean = i[-10:].split(": ")
        print(clean[1])
        i = float(clean[1])
        points.append(i)
    plt.xlabel("Dispatch Request Number")
    plt.ylabel("Sector Number ")
    plt.plot(idx, points, 'r-')
    plt.savefig(str(sys.argv[1]) + ".png")
    plt.show()


if __name__ == "__main__":
    assert(len(sys.argv) > 1), "Give me a file to read!"  # require a file
doWork(sys.argv[1])
