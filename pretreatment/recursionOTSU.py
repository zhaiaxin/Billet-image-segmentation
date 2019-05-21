# 1. use the threshold get by OTSU to perform THRESH_TOZERO with the target image
# 2. use THRESH_BINARY to make the img clearer
# 3. use median blur to remove noisy point
# 4. use morphological closed operation to close image
# 5. use vertical cut and max pixel value to decide whether to break the loop
# This looks like a lot of trouble, but there's no way to simplify it -_-

import cv2

from pretreatment.closeOperation import closure
from cutAlgorithm.verticalCut import vertical_cut
from util.imgManipulation import show_img_list


def recursion_otsu(img, path, name_suffix):
    flag = True
    # Convert a two-dimensional array to a one-dimensional array to facilitate future operations
    # array = np.ravel(img)

    # 1.use THRESH_TOZERO and THRESH_OTSU simultaneously, retval is the threshold get by OTSU
    retval, img = cv2.threshold(img, 0, 0, cv2.THRESH_TOZERO + cv2.THRESH_OTSU)

    while (flag):

        # 2.use THRESH_BINARY to make the img clearer,
        # The background is black(0) and the characters are white(255)
        _, img = cv2.threshold(img, retval, 255, cv2.THRESH_TOZERO)
        _, binary_img = cv2.threshold(img, retval, 255, cv2.THRESH_BINARY)

        # 3.Although there are many ways to remove noisy point
        # such as mean blur, box blur, gaussian blur, median blur
        # but for billet image, median blur is the best :)
        blur_img = cv2.medianBlur(binary_img, 3)

        # 4. use morphological closed operation to close image
        close_img = closure(blur_img)
        # cv2.imwrite(r"C:\Users\Administrator\Desktop\close.jpg",close_img)

        # if you want see the result get from each step, open the following two lines
        img_list = [img, binary_img, blur_img, close_img]
        show_img_list(img_list)

        retval += 1
        print("threshold :", retval)

        # 5.use vertical cut and max pixel value to decide whether to break the loop
        # if retval == max_pixel_value(img):
        if retval == 220:
            break
        flag = judge_flag(close_img, path, name_suffix)

    return close_img


def judge_flag(img, path, name_suffix):
    """ if the result's number of vertical cut is 5 or 6, break the loop """
    flag = True
    vertical_img = vertical_cut(img, path, name_suffix)

    if len(vertical_img) == 6 or len(vertical_img) == 5:
        flag = False

    return flag


# def max_pixel_value(img):
#     """ get max pixel value of the target image to decide whether to break the loop """
#     height, width = img.shape
#     maximum = 0
#
#     for i in range(height):
#         for j in range(width):
#             if img[i, j] > maximum:
#                 maximum = img[i, j]
#     return maximum


if __name__ == '__main__':
    img = cv2.imread(r"C:\Users\Administrator\Desktop\919251.jpg", cv2.IMREAD_GRAYSCALE)
    otsu_img = recursion_otsu(img, r"C:\Users\Administrator\Desktop", "scharr.jpg" )

