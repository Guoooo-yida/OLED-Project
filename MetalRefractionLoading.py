import csv
import os


def findName(name):
    waveLength = []
    real = []
    image = []
    for files in os.listdir(os.getcwd()):
        if ".csv" in files:
            if name in files:
                with open(files, encoding='utf-8-sig') as csvfile:
                    reader = csv.reader(csvfile)
                    row = [row for row in reader]

                    for i in range(len(row)):
                        waveLength.append(row[i][0])
                        real.append(row[i][1])
                        image.append(row[i][2])
                    for i in range(len(waveLength)):
                        waveLength[i] = 1000 * float(waveLength[i])
                        real[i] = float(real[i])
                        image[i] = float(image[i])
                break

    return waveLength, real, image


# findName('Al')
