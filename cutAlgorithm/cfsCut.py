# cfs(Connected field segmentation) is good way to solve vertical projection coincidence problem,
# but the implementation is complex, be prepared(!_!)

import queue
import numpy as np
import cv2

from util.split import split_dot


def cfs_cut(img, path, name_suffix):
    height, width = img.shape

    # visited represent a collection of accessed points
    visited = set()
    q = queue.Queue()

    # eight directions : up, down, left, right, top right, top left, bottom right, bottom left
    offset = [(0, 1), (0, -1), (-1, 0), (1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]
    cuts = []

    for x in range(height):
        for y in range(width):

            position = []

            if img[x, y] != 0 and (x, y) not in visited:
                q.put((x, y))
                position.append((x, y))
                visited.add((x, y))

            while not q.empty():
                x_p, y_p = q.get()

                for x_offset, y_offset in offset:
                    x_c, y_c = x_p + x_offset, y_p + y_offset

                    # avoid IndexOutOfBoundsException
                    if x_c < 0 or y_c < 0 or x_c >= height or y_c >= width:
                        continue

                    if (x_c, y_c) in visited:
                        continue

                    visited.add((x_c, y_c))

                    if img[x_c, y_c] != 0:
                        q.put((x_c, y_c))
                        position.append((x_c, y_c))

            if position:
                # Sort the position array by size y
                sort = sorted(position, key=lambda x: x[1])
                min_y, max_y = sort[0][1], sort[len(sort) - 1][1]
                # the width of the result which is smaller than 20 is noisy point
                if max_y - min_y > 20:
                    cuts.append(position)

    # Sort the results by the smallest y value:
    # 1.insert segmentation results the first element's y value, like this
    # [[(5,6),...,(7,7)], [(1,2),...,(3,3)], ..., [(10,11),...,(20,20)]]
    # ->
    # [[6,(5,6),...,(7,7)], [2,(1,2),...,(3,3)], ..., [11,(10,11),...,(20,20)]]

    for i in range(len(cuts)):
        cuts[i].insert(0, sorted(cuts[i], key=lambda x: x[1])[0][1])

    # 2.sort the results by the first element
    # [[2,(1,2),...,(3,3)], [6,(5,6),...,(7,7)], ..., [11,(10,11),...,(20,20)]]
    cuts_sort = sorted(cuts, key=lambda x: x[0])

    # 3.delete the first element
    # [[(1,2),...,(3,3)], [(5,6),...,(7,7)], ..., [(10,11),...,(20,20)]]
    for i in range(len(cuts_sort)):
        del cuts_sort[i][0]

    # Create a pure black region and assign the coordinates of the connected domains
    cfs_img = []
    for i in range(len(cuts_sort)):

        sort_x = sorted(cuts_sort[i], key=lambda x: x[0])
        sort_y = sorted(cuts_sort[i], key=lambda x: x[1])

        cuts_height = sort_x[len(sort_x) - 1][0] - sort_x[0][0]
        cuts_width = sort_y[len(sort_y) - 1][1] - sort_y[0][1]

        panel = np.zeros((cuts_height, cuts_width), dtype=np.uint8)
        for j in range(len(cuts_sort[i])):
            panel[cuts_sort[i][j][0] - sort_x[0][0] - 1, cuts_sort[i][j][1] - sort_y[0][1] - 1] = 255

        # For some reason, the new image will have burrs
        blur_img = cv2.medianBlur(panel, 5)

        cfs_img.append(blur_img)

    # name = split_dot(name_suffix)
    # for i in range(len(cfs_img)):
    #     cv2.imwrite(r"{}/{}'s {} part.jpg".format(path, name, i),
    #                 cfs_img[i])

    return cfs_img


if __name__ == '__main__':
    img = cv2.imread(r"C:\Users\Administrator\Desktop\close.jpg", cv2.IMREAD_GRAYSCALE)
    cfs_cut(img, r"C:\Users\Administrator\Desktop","close.jpg")