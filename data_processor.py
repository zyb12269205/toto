__author__ = 'yingbozhan'

import matplotlib.pyplot as plt
import numpy as np
import pylab as pl


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

import math
data = get_current()
min_key = min(data.keys())
max_key = max(data.keys())
counter = {v:0 for v in range(0, 7)}

for step in range(1,7):
  print step
  counter = {v:0 for v in range(0, 10)}
  for start in range(max_key, min_key+1, -1):
      start_set = set(data.get(start,[]))
      next_Set = set(data.get(start-step, [])+data.get(start-step-1, [])+data.get(start-step-2, []))
      counter[len(start_set.intersection(next_Set))] += 1
  print counter
  print {v:counter[v]*1.0/sum(counter.values()) for v in counter.keys()}










#import math
#data = get_current()
#data_av = {x:average_mean(data[x]) for x in data.keys()}
#data_ge = {x:geo_mean(data[x]) for x in data.keys()}
#data_ha = {x:harmony_average(data[x]) for x in data.keys()}
#
## pl.plot(range(0,len(data_av.keys())), sorted(data_av.values()))
## pl.plot(range(0,len(data_ge.keys())), sorted(data_ge.values()))
## pl.plot(range(0,len(data_ha.keys())), sorted(data_ha.values()))
#
#q1 = np.percentile(data_ge.values(), 25)
#q2 = np.percentile(data_ge.values(), 50)
#q3 = np.percentile(data_ge.values(), 75)
#print q1
#print q2
#print q3
#
##
## pl.show()
## x = data_ge.values()
## hist, bins = np.histogram(x, bins=20)
## width = 0.7 * (bins[1] - bins[0])
## center = (bins[:-1] + bins[1:]) / 2
## plt.bar(center, hist, align='center', width=width)
## plt.show()
##print sorted(data_geo.iteritems())
#
