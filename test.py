# -*- coding:utf-8 -*-
from fight import action, selection, endfind
import functions
import cv2


if 1:
    img = functions.screenshot()
    cv2.imwrite('1.jpg', img)
if 0:
    img = cv2.imread('1.jpg')
if 0:
    img1 = functions.cut_image(390, 485, 626, 960, img)
    cv2.imwrite('z.jpg', img1)
img = functions.screenshot()
cv2.imwrite('1.jpg', img)
print(endfind(img))