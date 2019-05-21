# Common edge detection methods include four operator:
# sobel, scharr, canny and Laplacian
# but for billet image, scharr is the best :)

import cv2

from util.imgManipulation import show_img_list


def scharr(img):

    # The x,y direction of the gradient
    scharrx = cv2.Scharr(img, cv2.CV_64F, 1, 0)
    scharry = cv2.Scharr(img, cv2.CV_64F, 0, 1)

    # Take the absolute value of the result
    scharrx = cv2.convertScaleAbs(scharrx)
    scharry = cv2.convertScaleAbs(scharry)

    scharrxy = cv2.addWeighted(scharrx, 0.5, scharry, 0.5, 0)

    return scharrxy

if __name__ == '__main__':

    img = cv2.imread(r"C:\Users\Administrator\Desktop\test.jpg",cv2.IMREAD_GRAYSCALE)
    scharr_img = scharr(img)

    img_list = [img, scharr_img]
    show_img_list(img_list)
    cv2.imwrite(r"C:\Users\Administrator\Desktop\scharr.jpg",scharr_img)