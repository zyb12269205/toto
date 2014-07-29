__author__ = 'yingbozhan'

import data_requester
import data_processor
from random import randrange


#data_requester.main()
#data_processor.main()
#data_processor.init_counter()

# drawno x - exclude up to x (not include drawno x)
def run_result_with_data(x=None, go_through=False):
    counter = 0
    result = []
    new_data = {}

    data = data_processor.get_current()

    if x is not None:
        for key in data.keys():
            if key < x:
                new_data[key] = data[key]
    else:
        new_data = data 

    stats = data_processor.init_stats(new_data)

    if x is not None and go_through:
        print x
        fail = data_processor.check(data[x],stats, new_data)
        print data_processor.FAIL_MSG.get(fail)

    if go_through: return [], fail
    for a in range(7,46):
        if a > stats['mean']['average'][1]: continue
        for b in range(a+1, 46):
            for c in range(b+1, 46):
                for d in range(c+1, 46):
                    for e in range(d+1, 46):
                        for f in range(e+1, 46):
                            if data_processor.check([a, b, c, d, e, f], stats, new_data)==0:
                                counter += 1
                                print([a, b, c, d, e, f])
                                result.append([a, b, c, d, e, f])
    return result, counter

def main():
    result, counter = run_result_with_data()
    
    

def verify_result(results, answer):
    performance = {v:0 for v in range(0,7)}
    for result in results:
        performance[len(set(result).intersection(set(answer)))] += 1
    return performance



def algorithm_test():
    test_round = 5
    data = data_processor.get_current()
    for key in sorted(data.keys(), reverse=True):
        if test_round <=0: break
        result, counter = run_result_with_data(key)
        performance = verify_result(result, data[key])
        print key
        print performance
        test_round -= 1

def big_prize_fail_test():
    data = data_processor.get_current()
    go_through = True
    performance = {v:0 for v in data_processor.FAIL_MSG.keys()}
    for key in sorted(data.keys(), reverse=True)[0:100]:
        result, counter = run_result_with_data(key, go_through)
        performance[counter] += 1
    for key in performance.keys():
        print data_processor.FAIL_MSG[key] + ": " + str(performance[key])



#algorithm_test()
#big_prize_fail_test()
main()



