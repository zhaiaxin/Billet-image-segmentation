import cv2
import numpy as np
import os
import datetime

from cutAlgorithm.dropCut import drop_cut
from cutAlgorithm.verticalCut import vertical_cut
from cutAlgorithm.horizontalCut import horizontal_cut
from cutAlgorithm.cfsCut import cfs_cut

from pretreatment.recursionOTSU import recursion_otsu
from pretreatment.scharrOperator import scharr

from util.split import split_slash, split_dot

RGB = [np.zeros(()), np.zeros(()), np.zeros(()), np.zeros(()), np.zeros(()), np.zeros(())]
STATE = True


def image_process(path_name_suffix):
    path, name_suffix = split_slash(path_name_suffix)

    img = cv2.imread(r"{}/{}".format(path, name_suffix), cv2.IMREAD_GRAYSCALE)

    scharr_img = scharr(img)

    close_img = recursion_otsu(scharr_img, path, name_suffix)

    horizontal_img = horizontal_cut(close_img)

    vertical_img = vertical_cut(horizontal_img, path, name_suffix)

    global RGB, STATE

    STATE = True
    if len(vertical_img) == 6:

        RGB = [cv2.cvtColor(vertical_img[0], cv2.COLOR_GRAY2BGR), cv2.cvtColor(vertical_img[1], cv2.COLOR_GRAY2BGR),
               cv2.cvtColor(vertical_img[2], cv2.COLOR_GRAY2BGR), cv2.cvtColor(vertical_img[3], cv2.COLOR_GRAY2BGR),
               cv2.cvtColor(vertical_img[4], cv2.COLOR_GRAY2BGR), cv2.cvtColor(vertical_img[5], cv2.COLOR_GRAY2BGR)]

    elif len(vertical_img) == 5:
        try:
            RGB, STATE = drop(vertical_img)

        except:
            STATE = False
            print("for {}, the drop algorithm failed to segment".format(name_suffix))
    else:

        cfs_img = cfs_cut(horizontal_img, path, name_suffix)

        if len(cfs_img) == 6:

            RGB = [cv2.cvtColor(cfs_img[0], cv2.COLOR_GRAY2BGR), cv2.cvtColor(cfs_img[1], cv2.COLOR_GRAY2BGR),
                   cv2.cvtColor(cfs_img[2], cv2.COLOR_GRAY2BGR), cv2.cvtColor(cfs_img[3], cv2.COLOR_GRAY2BGR),
                   cv2.cvtColor(cfs_img[4], cv2.COLOR_GRAY2BGR), cv2.cvtColor(cfs_img[5], cv2.COLOR_GRAY2BGR)]

        elif len(cfs_img) < 6:

            try:
                RGB[0:6], STATE = drop(cfs_img)
            except:
                STATE = False
                print("for {}, the drop algorithm failed to segment".format(name_suffix))
        else:
            STATE = False
            print("for {}, The connected domain algorithm divides more than 6 blocks".format(name_suffix))

    return RGB, STATE


def drop(adhension_img):
    global STATE
    STATE = True
    for i in range(len(adhension_img)):
        height, width = adhension_img[i].shape
        if width > 110:
            index = i
            adjoin_part = adhension_img[i]

    drop_img = drop_cut(adjoin_part)
    cv2.imwrite(r"C:/Users/Administrator/Desktop/adhension_img.jpg", adjoin_part)

    if len(drop_img) == 2:
        if index >= 1:  # 粘连部分在中间
            for i in range(index):
                RGB[i] = cv2.cvtColor(adhension_img[i], cv2.COLOR_GRAY2BGR)

        RGB[index] = cv2.cvtColor(drop_img[0], cv2.COLOR_GRAY2BGR)
        RGB[index + 1] = cv2.cvtColor(drop_img[1], cv2.COLOR_GRAY2BGR)

        if index + 2 <= 5:  # 粘连部分不是最后
            for j in reversed(range(index + 2, 6)):
                RGB[j] = cv2.cvtColor(adhension_img[j - 1], cv2.COLOR_GRAY2BGR)
    else:
        STATE = False

    return RGB, STATE


def batch_process(dir_path):
    success = 0
    fail = 0
    start_time = datetime.datetime.now()
    for name_suffix in os.listdir(dir_path):

        path_name = "{}/{}".format(dir_path, name_suffix)
        global STATE
        img, STATE = image_process(path_name)
        if STATE:

            name = split_dot(name_suffix)
            os.makedirs(r"{}/{}".format(dir_path, name))
            success += 1
            for i in range(6):
                cv2.imwrite(r"{}/{}/{}.jpg".format(dir_path, name, i), img[i])
        else:
            fail += 1
    end_time = datetime.datetime.now()
    time = (end_time - start_time).seconds
    print("success :", success)
    print("fail :", fail)
    return success, fail, time


if __name__ == '__main__':
    # image_process("C:/Users/Administrator/Desktop/917234.jpg")
    batch_process(r"C:/Users/Administrator/Desktop/wow")
