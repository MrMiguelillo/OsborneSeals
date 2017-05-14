import cv2
import paths

img_path = paths.path_to_imgs + '/1863-L119.M13/107/IMG_0002.png'

img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
img2 = cv2.GaussianBlur(img, (3, 3), 0)
# equ = cv2.equalizeHist(img)
bin_thresh, bin_img = cv2.threshold(img, 0, 1, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
bin_thresh, bin_img2 = cv2.threshold(img2, 0, 1, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
# bin_equ_t, bin_equ = cv2.threshold(equ, 0, 1, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)


se1 = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
se2 = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
mask = cv2.morphologyEx(bin_img, cv2.MORPH_CLOSE, se1)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, se2)
# mask /= 255

out = img * mask
out = (out > 5).astype('uint8')

# cv2.namedWindow("out", cv2.WINDOW_NORMAL)
# cv2.imshow("out", out*255)
# cv2.namedWindow("equ", cv2.WINDOW_NORMAL)
# cv2.imshow("equ", equ)
cv2.namedWindow("img", cv2.WINDOW_NORMAL)
cv2.imshow("img", bin_img*255)
cv2.namedWindow("img2", cv2.WINDOW_NORMAL)
cv2.imshow("img2", bin_img2*255)

cv2.waitKey()
