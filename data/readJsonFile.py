import json
import csv

fileName = 'document.json'

with open(fileName, 'rb') as fin:
    content = json.load(fin)
    count = 0
    data = ''
    for k, v in content.items():
        if k=='TimeStamp':
            date = v
        if k=='Categories':
            for k1, v1 in v.items():
                for p, cost in v1.items():
                    try:
                        f = open('today.csv', "a")
                        writer = csv.writer(f)
                        entries = [[p, date, cost]]
                        writer.writerows(entries)
                        f.close()
                    except:
                        pass
