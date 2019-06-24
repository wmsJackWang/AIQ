import csv
import math
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import numpy as np

def cross_table(data):
    counter = 0
    keys = {}
    for val in data:
        if val[0] not in keys:
            keys[val[0]] = counter
            counter += 1
        if val[1] not in keys:
            keys[val[1]] = counter
            counter += 1

    res = np.zeros([len(keys),len(keys)])

    for val in data:
        res[keys[val[0]]][keys[val[1]]] = val[2]

    print(res)

    with open('nice results.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        fieldnames = list(keys.keys())
        spamwriter.writerow(fieldnames)
        for ind, val in enumerate(res):
            name = list(keys.keys())[ind]
            spamwriter.writerow([name, *val])

        flat_list = [item for sublist in res for item in sublist]
        avg = 0.0
        cnt = 0.0
        for i in flat_list:
            if i == 0.0:
                continue   
            else:
                avg += i
                cnt += 1
        avg = avg/cnt

        spamwriter.writerow(('AVERAGE', avg))

    # See what data is missing (maximize everything)
    for ind,val in enumerate(res):
        for ind2,val2 in enumerate(val):
            if ind2 < ind:
                continue
            if val2 == 0.0:
                print(list(keys.keys())[ind],list(keys.keys())[ind2])
                

    plt.imshow(res, cmap='hot', interpolation='nearest')
    plt.show()

    return None


data = []

with open('d=1.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        data.append(row)

#print(data)

A = None
B = None
name1 = None
name2 = None
counter = 0
info = []

for ind, val in enumerate(data):
    if counter >= 3:
        counter = 0
    
    if counter == 0:
        name1 = val[0]
        A = float(val[2])

    elif counter == 1:
        name2 = val[0]
        B = float(val[2])

    elif counter == 2:
        Vmax = max(A,B)
        Vmin = min(A,B)
        V = float(val[2])
        if A == B:
            S = 0
        else:
            S = abs(abs(Vmax - V) - abs(Vmin - V) ) / abs( A  - B )
        info.append((name1, name2, S))         

    else:
        print('error')
        exit()

    counter += 1
    continue

cross_table(info)

