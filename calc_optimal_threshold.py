import csv

ratios = []

with open('data/results_no_seals.txt', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        ratio = row[2].replace("\'", "")
        ratios.append(float(ratio))
        print(row[2])

print(ratios)
