__author__ = 'yingbozhan'

####################
# Cron Job to trigger update every day
# 1. update: Verify with Max + 1 ==> No result, No update
# 2. init: Init the whole data_requester with data stored in csv file
####################

import unicodedata
import urllib
import urllib2
import re
import json
import time

def get_config():
    f = open('config', 'r')
    configs = {}
    for config_read in f.readlines():
        parts = config_read.split(':')
        configs[parts[0].strip(' \n')] = parts[1].strip(' \n')
    f.close()
    return configs


def update_config(configs):
    f = open('config', 'w')
    content = ''
    for key in configs.keys():
        content += key + ':' + configs[key] + '\n'
    f.write(content)
    f.close()

def get_current():
    f = open('data', 'r')
    data = {}
    for oneday in f.readlines():
        parts = oneday.split(',')
        if parts[0] not in data.keys() or (parts[0] in data.keys() and len(parts[1:-1])> len(data[parts[0]])):
            data[int(parts[0])] = [int(v) for v in parts[1:-1]]
    f.close()
    print data
    return data


def update_current(data):
    f = open('data', 'w')
    content = ''
    for key in data.keys():
        content += str(key) + ','
        for value in data[key]:
            content += str(value) + ','
        content += '\n'
    f.write(content)
    f.close()


def add_data(data, new_data):
    data.update(new_data)
    update_current(data)


def http_request_with_drawno(drawno):
    url = 'http://www.singaporepools.com.sg/_Layouts/TotoApplication/TotoCommonPage.aspx/getTotoResultByDrawNumber'
    values = {'lang': 'en',
              'drawno': drawno, }
    headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
               'Content-Type': 'application/json; charset=utf-8'}

    data = json.dumps(values)
    req = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(req)
    time.sleep(1)
    return response.read()


def process(raw_http_response):
    http_response = raw_http_response.decode("unicode-escape")
    print http_response
    http_response_parts = http_response.split('\n')
    win = []
    for response in http_response_parts:
        if "winning_numbers_toto_b" not in response: continue
        try:
            regex = re.compile(">\d[0-9]?<")
            raw_win = regex.findall(response)
            win.extend([ball[1:-1] for ball in raw_win])
        except:
            return None
    if len(win) == 7:
        return win
    else:
        return None


def get_update_on(drawno):
    return process(http_request_with_drawno(drawno))


def main():
    configs = get_config()
    max_drawno = max(2965, configs.get('max_drawno', 0))
    min_drawno = min(2652, configs.get('min_drawno', 0))
    update_on = min_drawno
    data = get_current()
    counter = 50
    while counter > 0:
        if data.get(update_on, None) is not None:
          update_on += 1
          continue
        value = get_update_on(update_on)
        if value is not None and data.get(update_on,None) is not None and len(data[update_on]) ==7:
            pass
        elif value is not None and len(value) == 7:
            data[update_on] = value
        else:
            break
        counter -= 1
        update_on += 1
    update_current(data)


def clear_data():
    data = get_current()
    new_data = {}
    for key in data.keys():
        if new_data.get(key, None) is None:
            new_data[key] = data[key]
        elif len(new_data[key]) < len(data[key]):
                new_data[key] = data[key]
        else:
            pass
    update_current(new_data)


#clear_data()
#print get_update_on(2753)
#main()


def debug():
    configs = get_config()
    data = get_current()
    update_on_list = ['2770','2786','2750','2929','2959','2753','2874']

    for update_on in update_on_list:
        value = get_update_on(update_on)
        if value is not None and data.get(update_on,None) is not None and len(data[update_on]) ==7:
            pass
        elif value is not None and len(value) == 7:
            data[update_on] = value
        else:
            break
    update_current(data)
