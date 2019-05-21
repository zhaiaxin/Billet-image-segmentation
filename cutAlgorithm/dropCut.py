# it's just a simple implementation of drop algorithm
# I have to admit this is not a good partition -_-

import cv2
import numpy as np

from util.imgManipulation import show_img_list

temp = [0, 0, 0]


def vertical_project(img):
    """ get a third of the length of the vertical projection """

    # use pix list to save the sum of each column
    pix = list(np.sum(np.array(img), axis=0))

    # use non_zero list to save the sum of each column, which is bigger than a particular value
    non_zero = []

    for i in range(len(pix)):
        if pix[i] > 0:
            non_zero.append(i)

    third = (min(non_zero) + max(non_zero)) // 3
    return third


def start_point(img, third):
    """ get the coordinates of the initial drop point"""

    height, width = img.shape

    flag = False
    # avoid cutting errors due to burrs on the top of the image
    for i in range(height // 8, height):
        for j in range(third, width):

            # find the first point in queue
            # like this, 01*110 (0 - white, 1 - black, 1* - target point)
            if img[i, j - 1] > 0 and img[i, j] == 0:
                origin = j

                while img[i, j] == 0 and j < width - 1:
                    j += 1

                gap = j - origin

                if gap > 5:
                    flag = True
                    break
        if flag:
            break

    return i, origin


def drop_rule(img, i, j):
    """ get the drop rule which selected according to the distribution of surrounding points """

    rule = 1

    left = img[i, j - 1]
    right = img[i, j + 1]
    down = img[i + 1, j]
    bottom_left = img[i + 1, j - 1]
    bottom_right = img[i + 1, j + 1]
    location = [bottom_left, down, bottom_right, right, left]

    if location[1] == 0:
        rule = 1
    elif location[1:3] == [255, 0]:
        rule = 2
    elif location[0:3] == [0, 255, 255]:
        rule = 3
    elif location[0:4] == [255, 255, 255, 0]:
        rule = 4
    elif location[0:5] == [255, 255, 255, 255, 0]:
        rule = 5
    elif location[0] == [255] and location[2:5] == [255, 255, 255]:
        rule = 6

    return rule


def drop_action(rule, i, j, n):
    """ get the coordinate of next point by rule"""

    # save the drop rule for the last three points
    global temp

    if n % 3 == 1:
        temp[0] = rule
    elif n % 3 == 2:
        temp[1] = rule
    elif n % 3 == 0:
        temp[2] = rule

    # let the water drop drop as it circulates from side to side
    if temp == [4, 5, 4] or temp == [5, 4, 5]:
        rule = 3

    if rule == 1 or rule == 6:
        i += 1
    elif rule == 2:
        i += 1
        j += 1
    elif rule == 3:
        i += 1
        j -= 1
    elif rule == 4:
        j += 1
    elif rule == 5:
        j -= 1

    return i, j


def drop_way(img, i, j):
    """ get the trail of the drop"""
    way = []
    n = 1
    height, width = img.shape

    while i in range(height - 1) and j in range(width - 1):

        rule = drop_rule(img, i, j)
        i, j = drop_action(rule, i, j, n)
        n += 1
        way.append((i, j))

    return way


def drop_split(img, way):
    """ cut the image """

    height, width = img.shape

    # get the maximum and minimum width of the way
    way.sort(key=lambda x: x[1])
    minimum = way[0][1]
    maximum = way[len(way) - 1][1]

    left_img = img[0:height, 0:maximum]
    right_img = img
    for i in range(len(way)):
        y = way[i][0]
        x = way[i][1]

        # if you want to see the trail of the drop, open the following 2 lines
        # img[y][x - 5:x] = 128
        # img[y][x:x + 5] = 128

        # set pixel value of the adhesive part to 0
        for j in range(maximum - x):
            b = x + j
            left_img[y, x + j] = 0
        for k in range(x - minimum):
            a = x - k
            right_img[y, x - k] = 0

    right_img = img[0:height, minimum:width]

    return left_img, right_img


def drop_cut(img):
    """ The total logic of the dripping algorithm """

    mid = vertical_project(img)
    i, j = start_point(img, mid)
    way = drop_way(img, i, j)
    left_img, right_img = drop_split(img, way)

    return left_img, right_img


if __name__ == '__main__':
    img = cv2.imread(r"C:\Users\Administrator\Desktop\horizontal.jpg", cv2.IMREAD_GRAYSCALE)

    left_img, right_img = drop_cut(img)
    img_list = [img, left_img, right_img]
    show_img_list(img_list)
