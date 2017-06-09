fname = 'today.csv'
import csv

with open(fname) as f:
    
    content = csv.reader(f)
    for row in content:
        print row[0]
