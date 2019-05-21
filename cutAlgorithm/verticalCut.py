# vertical_cut is the simplest algorithm of image cutting
# But there are a few caveats, which is annotated :)
import numpy as np
import cv2

from util.split import split_dot


def vertical_cut(img, path, name_suffix):
    _, width = img.shape

    # use pix list to save the sum of each column
    pix = list(np.sum(np.array(img), axis=0))

    # use non_zero list to save the sum of each column, which is bigger than a particular value
    non_zero = []

    for i in range(len(pix)):
        # 1275 = 255 * 5
        if pix[i] > 1275:
            non_zero.append(i)

    segment_list = []
    segment_list.append(non_zero[0])

    for i in range(1, len(non_zero)):
        if abs(non_zero[i] - non_zero[i - 1]) > 1:
            segment_list.extend([non_zero[i - 1], non_zero[i]])

    segment_list.append(non_zero[-1])

    # avoid the effect of single column noisy point
    # like this: 1,2,3, 5,6,7, 11, 20,21,22
    # 11 is the single column noisy point
    segment_list = remove_repetition(segment_list)

    vertical_img = []
    for i in range(len(segment_list) // 2):
        # the width of the result is bigger than 20
        if segment_list[i * 2 + 1] - segment_list[i * 2] > 20:
            vertical_img.append(img[0:width, segment_list[i * 2]:segment_list[i * 2 + 1]])

    name = split_dot(name_suffix)
    for i in range(len(vertical_img)):
        cv2.imwrite(r"{}/{}'s {} part.jpg".format(path, name, i),
                    vertical_img[i])

    return vertical_img


def remove_repetition(img_list):
    """ remove the repetition element of the list """
    repetition = []
    for i in range(1, len(img_list)):
        if img_list[i] == img_list[i - 1]:
            repetition.append(img_list[i])

    for i in range(len(repetition)):
        img_list.remove(repetition[i])
        img_list.remove(repetition[i])

    return img_list


if __name__ == '__main__':
    img = cv2.imread(r"C:\Users\Administrator\Desktop\close.jpg", cv2.IMREAD_GRAYSCALE)
    vertical_cut(img, r"C:\Users\Administrator\Desktop", "close.jpg")
