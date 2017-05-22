import sys
import os


def testStuff():
    fOpen = open("testFile.txt", "w+")
    fOpen.write("I hate the Linux Kernel! ~Brandon \n")
    os.rename("testFile.txt", "~/testFile.txt")
    fOpen.close()


if __name__ == "__main__":
    if (len(sys.argv) < 2):
        raise("No file path specified, please insert CLA, EXITING! \n")
    print(sys.argv[1])
    testStuff()
