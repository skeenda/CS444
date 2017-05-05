import os


def writeFiles(i):
    f = open("IOFILE" + str(i) + ".txt", "a+")
    f.write("SOME IO!!! From file " + str(i))
    f.close()


if __name__ == "__main__":
    fileNames = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    a = 1
    while(True):
        # if counter gets to 25 remove all files so they don't get too big.
        if (a % 25 == 0):
            for j in fileNames:
                os.remove("IOFILE" + str(j) + ".txt")
        for j in fileNames:
            writeFiles(j)
            f = open("IOFILE" + str(j) + ".txt")
            data = f.read()
            f.close()
            a += 1  # inc counter
            print (data + "\n")
