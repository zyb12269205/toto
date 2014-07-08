__author__ = 'yingbozhan'

import matplotlib.pyplot as plt
import numpy as np

def get_current():
    f = open('data', 'r')
    data = {}
    for oneday in f.readlines():
        parts = oneday.split(',')
        if len(parts) !=9:
            continue
        data[int(parts[0])] = [int(x) for x in parts[1:-1]]
    f.close()
    print data
    return data

def geo_mean(list_int):
    product = 1
    if len(list_int) == 0: return 1
    for x in list_int:
        product *= x
    return math.pow(x, 1.0/len(list_int))

import math
data = get_current()
data_geo = {x:geo_mean(data[x]) for x in data.keys()}
x = data_geo.values()
hist, bins = np.histogram(x, bins=50)
width = 0.7 * (bins[1] - bins[0])
center = (bins[:-1] + bins[1:]) / 2
plt.bar(center, hist, align='center', width=width)
plt.show()
print sorted(data_geo.iteritems())

