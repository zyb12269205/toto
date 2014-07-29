__author__ = 'yingbozhan'

import matplotlib.pyplot as plt
import numpy as np
import pylab as pl
import math
import operator


TRACE_BACK_START_MAX = 20
TRACE_BACK_STEP_MAX = 10

def get_current():
  f = open('data', 'r')
  data = {}
  for oneday in f.readlines():
    parts = oneday.split(',')
    if len(parts) != 9:
      continue
    data[int(parts[0])] = [int(x) for x in parts[1:-1]]
  f.close()
  return data


def geo_mean(list_int):
  product = 1
  if len(list_int) == 0: return 1
  for x in list_int:
    product *= x
  return math.pow(product, 1.0 / len(list_int))


def average_mean(list_int):
  sum_all = 0
  if len(list_int) == 0: return -1
  for x in list_int:
    sum_all += x
  return sum_all / len(list_int)


def harmony_average(list_int):
  sum_all = 0
  if len(list_int) == 0: return 1
  for x in list_int:
    sum_all += 1.0 / x
  return len(list_int) * 1.0 / sum_all


def init_counter(data):
  counter = {v: {} for v in range(1, TRACE_BACK_START_MAX)}
  for v in counter:
    counter[v] = {x: [0, 0, 0, 0, 0, 0, 0, 0] for x in range(1, TRACE_BACK_STEP_MAX + 1)}

  for draw in range(max(data.keys()), min(data.keys()), -1):
    sample_set = set(data.get(draw, []))
    if len(sample_set) == 0: continue
    for start in range(1, TRACE_BACK_START_MAX):
      find_all = False
      test_list = []
      for step in range(1, TRACE_BACK_STEP_MAX):
        test_list += data.get(draw - step - start, [])
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


def init_least(data):
  least = {v: 0 for v in range(1, 46)}
  for key in data.keys():
    for x in data[key]:
      least[x] += 1
  sorted_x = sorted(least.iteritems(), key=operator.itemgetter(1))
  return [sorted_x[i][0] for i in range(0, 9)]


def init_least_most(data):
  least = {v: 0 for v in range(1, 46)}
  for key in data.keys():
    for x in data[key]:
      least[x] += 1
  sorted_x = sorted(least.iteritems(), key=operator.itemgetter(1))
  return [sorted_x[i][0] for i in range(0, 45)]


def init_most(data):
  least = {v: 0 for v in range(1, 46)}
  for key in data.keys():
    for x in data[key]:
      least[x] += 1
  sorted_x = sorted(least.iteritems(), key=operator.itemgetter(1))
  return [sorted_x[i][0] for i in range(36, 45)]


def init_diff(data):
  least = {v: 0 for v in range(0, 46)}
  for key in data.keys():
    for x in data[key]:
      for y in data[key]:
        least[abs(x - y)] += 1
  sorted_x = sorted(least.iteritems(), key=operator.itemgetter(1))
  print len(sorted_x)
  return [sorted_x[i][0] for i in range(36, 45)]


def init_trend(data):
  trend = {v: [] for v in range(1, 46)}
  for key in sorted(data.keys()):
    value = sorted(data[key])
    next_value = sorted(data.get(key + 1, []))
    if len(next_value) == 0: continue
    for index in range(0, 6):
      trend[value[index]].append(next_value[index])
  for key in trend.keys():
    detail = trend[key]
    detail_occ = {x: detail.count(x) for x in set(detail)}
    sorted_x = sorted(detail_occ.iteritems(), key=operator.itemgetter(1))
    trend[key] = [sorted_x[i][0] for i in range(0, min(len(sorted_x), 1))]
  return trend


def init_odd_even(data):
  count_odd = {v: 0 for v in range(0, 8)}
  for key in data:
    local_count = 0
    for x in data[key]:
      if x % 2 == 1:
        local_count += 1
    count_odd[local_count] += 1
  sorted_x = sorted(count_odd.iteritems(), key=operator.itemgetter(1))
  return [sorted_x[i][0] for i in range(5, 8)]


def init_stats(data):
  stats = {}
  stats['counter'] = init_counter(data)
  stats['mean'] = init_mean(data)
  stats['least'] = init_least(data)
  stats['diff'] = init_diff(data)
  stats['trend'] = init_trend(data)
  stats['most'] = init_most(data)
  stats['least_most'] = init_least_most(data)
  stats['odd_even'] = init_odd_even(data)
  #print stats
  return stats


def occ_check(sample, counter, data):
  test_list = []
  sample_set = set(sample)
  draw = max(data.keys())
  for start in range(1, TRACE_BACK_START_MAX):
    find_all = False
    test_list = []
    for step in range(1, TRACE_BACK_STEP_MAX):
      test_list += data.get(draw - step - start, [])
      if counter[start][step][len(sample_set.intersection(set(test_list)))] < 10:
        return False
      if sample_set.issubset(set(test_list)):
        find_all = True
        break
    if not find_all and counter[start][TRACE_BACK_STEP_MAX][len(sample_set.intersection(set(test_list)))] < 5:
      return False
  return True


def mean_average_check(sample, mean, data):
  sample_av = average_mean(sample)
  prod_av = (sample_av - mean['average'][0]) * (sample_av - mean['average'][1])
  if prod_av > 0:
    return False
  return True


def mean_geo_check(sample, mean, data):
  sample_ge = geo_mean(sample)
  prod_ge = (sample_ge - mean['geo'][0]) * (sample_ge - mean['geo'][1])
  if prod_ge > 0:
    return False
  return True


def mean_harmony_check(sample, mean, data):
  sample_ha = harmony_average(sample)
  prod_ha = (sample_ha - mean['harmony'][0]) * (sample_ha - mean['harmony'][1])
  if prod_ha > 0:
    return False
  return True


def least_check(sample, least_occ, data):
  if len(set(sample).intersection(set(least_occ))) >= 1:
    return True
  else:
    return False


def most_check(sample, most_occ, data):
  if len(set(sample).intersection(set(most_occ))) >= 1:
    return True
  else:
    return False


def least_most_check(sample, occ, data):
  for i in range(0, 5):
    if len(set(sample).intersection(set(occ[i * 9:i * 9 + 9]))) >= 1:
      continue
    else:
      return False
  return True


def diff_check(sample, diff, data):
  count = 0
  for x in sample:
    for y in sample:
      if abs(x - y) in diff:
        count += 1
  if count > 16 :
    return True
  return False


def trend_check(sample, trend, data):
  last_occ_result = sorted(data[max(data.keys())])
  sorted_sample = sorted(sample)
  count = []

  for remove_index in range(0, 7):
    local_count = 0
    last_occ_result_update = [last_occ_result[i] for i in range(0, 7) if i != remove_index]
    possible_occs = [trend[last_occ_result_update[i]] for i in range(0, 6)]
    for compare_sample_index in range(0, 6):
      if sorted_sample[compare_sample_index] in possible_occs[compare_sample_index]:
        local_count += 1
    count.append(local_count)

  if max(count) == 2:
    return True
  return False


def odd_even_check(sample, odd, data):
  local_count = 0
  for x in sample:
    if x % 2 == 1:
      local_count += 1
  if local_count in odd:
    return True
  else:
    return False

FAIL_MSG = {
  0: "success",
  -1: 'least_check',
  -2: 'diff_check',
  -3: 'trend_check',
  -4: 'occ_check',
  -5: 'mean_average_check',
  -6: 'mean_geo_check',
  -7: 'mean_harmony_check',
  -8: 'most_check',
  -9: 'least_most_check',
  -10: 'odd_even_check'
}

def check(sample, stats, data):
  if not trend_check(sample, stats['trend'], data):
    return -3

  if not odd_even_check(sample, stats['odd_even'], data):
    return -10

  if not least_most_check(sample, stats['least_most'], data):
    return -9

  if not diff_check(sample, stats['diff'], data):
    return -2

  if not mean_average_check(sample, stats['mean'], data):
    #print 'fail mean' + str(sample)
    return -5

  if not mean_geo_check(sample, stats['mean'], data):
    #print 'fail mean' + str(sample)
    return -6

  if not mean_harmony_check(sample, stats['mean'], data):
    #print 'fail mean' + str(sample)
    return -7

  if not occ_check(sample, stats['counter'], data):
  #print 'fail occ ' + str(sample)
    return -4

  return 0




