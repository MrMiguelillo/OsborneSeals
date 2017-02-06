import csv
import numpy as np

isFirst = True
ratios = []
with open('sql scripts/OdobleC_in_docs_and_results.csv', newline='') as csvfile:
    o2c_data = csv.reader(csvfile, quotechar='|')
    for row in o2c_data:
        if not isFirst:
            if row[0] == '"O Doble C"':
                try:
                    ratios.append(float(row[2]))
                except ValueError:
                    print("error: non-numeric or non-float number")
        else:
            isFirst = False

print(np.average(ratios))
print(np.max(ratios))
print(np.min(ratios))
