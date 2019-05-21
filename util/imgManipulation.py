import cv2
import numpy as np


def show_img_list(img_list):
    if isinstance(img_list, np.ndarray):
        cv2.imshow("all", img_list)

    elif isinstance(img_list, list):
        for i in range(len(img_list)):
            cv2.imshow("{}".format(i), img_list[i])

    cv2.waitKey()
    cv2.destroyAllWindows()