# horizontal_cut is so simple that I believe u can understand it quickly :)

import numpy as np
import cv2

from util.imgManipulation import show_img_list


def horizontal_cut(img):
    _, width = img.shape

    # axis : 0 is column, 1 is row
    pix = list(np.sum(np.array(img), axis=1))

    non_zero = []

    for i in range(len(pix)):
        #  1275 = 255 * 5
        if pix[i] >= 1275:
            non_zero.append(i)

    seg_img = img[non_zero[0]:non_zero[-1], 0:width]

    return seg_img


if __name__ == '__main__':
    img = cv2.imread(r"C:\Users\Administrator\Desktop\the close.jpg 's 4 character.jpg", cv2.IMREAD_GRAYSCALE)
    horizontal_img = horizontal_cut(img)
    img_list = [img, horizontal_img]
    show_img_list(img_list)
    cv2.imwrite(r"C:\Users\Administrator\Desktop\horizontal.jpg", horizontal_img)