import math
import pylab as pl
import random

def geo_mean(list_int):
    product = 1
    if len(list_int) == 0: return 1
    for x in list_int:
        product *= x
    return math.pow(x, 1.0/len(list_int))

def average_mean(list_int):
    sum_all = 0
    if len(list_int) == 0: return 1
    for x in list_int:
        sum_all += x
    return sum_all/len(list_int)

def harmony_average(list_int):
    sum_all = 0
    if len(list_int) == 0: return 1
    for x in list_int:
        sum_all += 1.0/x
    return len(list_int)*1.0/sum_all


test_sample = 300
sample = range(1, 46)

data = {x:random.sample(sample,7) for x in range(0, test_sample)}
data_av = {x:average_mean(data[x]) for x in data.keys()}
data_ge = {x:geo_mean(data[x]) for x in data.keys()}
data_ha = {x:harmony_average(data[x]) for x in data.keys()}

pl.plot(range(0,len(data_av.keys())), sorted(data_av.values()))
pl.plot(range(0,len(data_ge.keys())), sorted(data_ge.values()))
pl.plot(range(0,len(data_ha.keys())), sorted(data_ha.values()))
pl.show()
