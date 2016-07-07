import cv2.xfeatures2d as xf
import cv2


img_path = 'C:/Users/usuario/Documents/Lab_Osborne/Fotos_sellos'
surf = xf.SURF_create(500)

for i in range(1, 6):
    img = cv2.imread('%s/tomas_osborne%d_train.png' % (img_path, i))
    kp, des = surf.detectAndCompute(img, None)
    print(len(kp))


