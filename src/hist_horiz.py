import cv2
import matplotlib.pyplot as plt
from src import Splitting

split = Splitting.Splitting()


def separar_columnas(histograma):
    long = histograma.size
    lower_index = round(long/3, 0)
    upper_index = round(2*long/3, 0)
    suma = 0
    racha = 0
    max_racha = 0
    curr_gap_lower_x = 99999999999
    curr_gap_upper_x = 0
    prev_gap_lower_x = 99999999999
    prev_gap_upper_x = 0
    for x in range(int(lower_index), int(upper_index)):
        if histograma[x] <= 10:
            suma += 1
            if curr_gap_lower_x >= 99999:
                curr_gap_lower_x = x
        else:
            racha = suma
            suma = 0
            curr_gap_upper_x = x

        if racha > max_racha:
            max_racha = racha
            prev_gap_lower_x = curr_gap_lower_x
            prev_gap_upper_x = curr_gap_upper_x

    res_x = round((prev_gap_upper_x - prev_gap_lower_x)/2, 0) + prev_gap_lower_x
    return int(res_x)


img = cv2.imread('../met_1_vec_0_sig_-1_thr_180_binImg.png', 0)

hist = split.hor_hist(img)
plt.plot(hist)
plt.show()

divx = separar_columnas(hist)
print(divx)

cv2.line(img, (divx, 0), (divx, 10000), 100, 5)
cv2.namedWindow('result', cv2.WINDOW_NORMAL)
cv2.imshow('result', img)

cv2.waitKey()
cv2.destroyAllWindows()

