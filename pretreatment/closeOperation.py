# Morphological closed operations are first expanded and then corroded
# it has 3 types of kernel:
# MORPH_RECT, MORPH_ELLIPSE, MORPH_CROSS

# but for billet image,
# the MORPH_ELLIPSE is the best :)

import cv2

from util.imgManipulation import show_img_list


def closure(img):
    # The larger the kernel, the better the closure
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
    closed_img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

    return closed_img


if __name__ == '__main__':
    img = cv2.imread(r"C:\Users\Administrator\Desktop\test.jpg", cv2.IMREAD_GRAYSCALE)
    closed_img = closure(img)

    img_list = [img, closed_img]
    show_img_list(img_list)
