import cv2
import matplotlib.pyplot as plt

original = cv2.imread('../imgs/Narciso2.png')

results = []
with open('../T_1892.01.25_erosion_3.txt') as inputfile:
    for line in inputfile:
        results.append(line.strip().split('\t'))

for z in range (0, len(results)):

    if int(results[z][1]) == 1:

        cv2.line(original, (int(results[z][3]), int(results[z][4])), (int(results[z][5]), int(results[z][4])), 0, 1)
        cv2.line(original, (int(results[z][3]), int(results[z][4])), (int(results[z][3]), int(results[z][6])), 0, 1)
        cv2.line(original, (int(results[z][5]), int(results[z][4])), (int(results[z][5]), int(results[z][6])), 0, 1)
        cv2.line(original, (int(results[z][3]), int(results[z][6])), (int(results[z][5]), int(results[z][6])), 0, 1)

cv2.namedWindow('result', cv2.WINDOW_AUTOSIZE)
cv2.imshow('result', original)
cv2.imwrite('../groundtruth.png', original)

plt.figure(1)
plt.show()
