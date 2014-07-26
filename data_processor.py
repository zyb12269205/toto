__author__ = 'yingbozhan'

import matplotlib.pyplot as plt
import numpy as np
import pylab as pl
import math
TRACE_BACK_START_MAX = 10
TRACE_BACK_STEP_MAX = 6
def get_current():
    f = open('data', 'r')
    data = {}
    for oneday in f.readlines():
        parts = oneday.split(',')
        if len(parts) !=9:
            continue
        data[int(parts[0])] = [int(x) for x in parts[1:-1]]
    f.close()
    return data

def geo_mean(list_int):
    product = 1
    if len(list_int) == 0: return 1
    for x in list_int:
        product *= x
    return math.pow(product, 1.0/len(list_int))

def average_mean(list_int):
    sum_all = 0
    if len(list_int) == 0: return -1
    for x in list_int:
        sum_all += x
    return sum_all/len(list_int)

def harmony_average(list_int):
    sum_all = 0
    if len(list_int) == 0: return 1
    for x in list_int:
        sum_all += 1.0/x
    return len(list_int)*1.0/sum_all

def init_counter(data):
    counter = {v:{} for v in range(1, TRACE_BACK_START_MAX)}
    for v in counter:
        counter[v] = {x:[0,0,0,0,0,0,0,0] for x in range(1, TRACE_BACK_STEP_MAX+1)}

    for draw in range(max(data.keys()), min(data.keys()), -1):
        sample_set = set(data.get(draw, []))
        if len(sample_set) == 0: continue
        for start in range(1, TRACE_BACK_START_MAX):
            find_all = False
            test_list = []
            for step in range(1,TRACE_BACK_STEP_MAX):
                test_list += data.get(draw-step-start, [])
                counter[start][step][len(sample_set.intersection(set(test_list)))] += 1
                if sample_set.issubset(set(test_list)):
                    find_all = True
                    break
            if not find_all:
                counter[start][TRACE_BACK_STEP_MAX][len(sample_set.intersection(set(test_list)))] += 1
    return counter

def init_mean(data):
    data_av = [average_mean(data[x]) for x in data.keys()]
    data_ge = [geo_mean(data[x]) for x in data.keys()]
    data_ha = [harmony_average(data[x]) for x in data.keys()]
    mean = {}
    mean['average'] = [np.percentile(data_av, 20), np.percentile(data_av, 80)]
    mean['geo'] = [np.percentile(data_ge, 20), np.percentile(data_ge, 80)]
    mean['harmony'] = [np.percentile(data_ha, 20), np.percentile(data_ha, 80)]
    return mean

def init_stats(data):
    stats = {}
    stats['counter'] = init_counter(data)
    stats['mean'] = init_mean(data)
    return stats


def occ_check(sample, counter, data):
    test_list = []
    sample_set = set(sample)
    draw = max(data.keys())
    for start in range(1, TRACE_BACK_START_MAX):
        find_all = False
        test_list = []
        for step in range(1,TRACE_BACK_STEP_MAX):
            test_list += data.get(draw-step-start, [])
            if counter[start][step][len(sample_set.intersection(set(test_list)))] == 0:
                return False
            if sample_set.issubset(set(test_list)):
                find_all = True
                break
        if not find_all and counter[start][TRACE_BACK_STEP_MAX][len(sample_set.intersection(set(test_list)))]== 0:
            return False
    return True

def mean_check(sample, mean, data):
    sample_av = average_mean(sample)
    sample_ge = geo_mean(sample)
    sample_ha = harmony_average(sample)
    prod_av = (sample_av - mean['average'][0]) * (sample_av - mean['average'][1])
    prod_ge = (sample_ge - mean['geo'][0]) * (sample_ge - mean['geo'][1])
    prod_ha = (sample_ha - mean['harmony'][0]) * (sample_ha - mean['harmony'][1])
    if prod_av > 0 or prod_ge > 0 or prod_ha > 0:
        return False
    return True

def check(sample, stats, data):
    if not mean_check(sample, stats['mean'],data):
        #print 'fail mean' + str(sample)
        return False
    if not occ_check(sample, stats['counter'], data):
        #print 'fail occ ' + str(sample)
        return False

    return True




