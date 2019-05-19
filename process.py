import cv2
import numpy as np
import queue
import os
import datetime

from dropCut import drop_cut

RGB = [np.zeros(()), np.zeros(()), np.zeros(()), np.zeros(()), np.zeros(()), np.zeros(())]
STATE = True


def scharr(img):
    scharrx = cv2.Scharr(img, cv2.CV_64F, 1, 0)  # x方向梯度
    scharry = cv2.Scharr(img, cv2.CV_64F, 0, 1)  # y方向梯度

    scharrx = cv2.convertScaleAbs(scharrx)  # x的绝对值
    scharry = cv2.convertScaleAbs(scharry)  # y的绝对值

    scharrxy = cv2.addWeighted(scharrx, 0.5, scharry, 0.5, 0)  # x与y相加

    return scharrxy


def recursionOTSU(img, n):
    array = np.ravel(img)  # 将 二维数组img 降维为 一维数组array

    for i in range(n):
        retval, array = cv2.threshold(array, 0, 0, cv2.THRESH_TOZERO + cv2.THRESH_OTSU)  # 对 array 同时进行 阈值化为0 和 OTSU算法

        array = array[array > 0]  # 将 array 中等于0的元素去除掉

        retval, img = cv2.threshold(img, retval, 0, cv2.THRESH_TOZERO)  # 用新的阈值对图像进行 阈值化为0 的操作

    return img, retval


def horizontalCut(img):
    _, height = img.shape

    pix = list(np.sum(np.array(img), axis=1))  # axis = 1，表示按行

    nonZero = []  # 列表保存像素累加值大于0的行

    for i in range(len(pix)):
        if pix[i] >= 5100:  # 可能会有少数点分布，所以总和大于 20 * 255 = 5100
            nonZero.append(i)

    segImg = img[nonZero[0]:nonZero[-1], 0:height]

    return segImg


def verticalCut(img, filename, path):
    _, height = img.shape

    pix = list(np.sum(np.array(img), axis=0))  # pix存储每一列像素的和

    nonZero = []  # 列表保存像素累加值大于0的列

    for i in range(len(pix)):  # len(pix)代表总共有多少列，也就是图像的宽度
        if pix[i] > 255:  # 去除噪点
            nonZero.append(i)  # 加入一个对象

    segList = []  # 保存所有的边界
    segList.append(nonZero[0])  # 保存第一个大于0的列

    for i in range(1, len(nonZero)):
        if abs(nonZero[i] - nonZero[i - 1]) > 1:  # 将前一个数字最后一点的坐标，与后一个数字第一个点的坐标记录下来
            segList.extend([nonZero[i - 1], nonZero[i]])  # 加入一个序列

    segList.append(nonZero[-1])  # 保存最后一个大于0的列

    verticalImg = []
    for i in range(len(segList) // 2):
        # cv2.imwrite(r"{}\the {} 's {} character.jpg".format(path, filename, i),
        #             img[0:height, segList[i * 2]:segList[i * 2 + 1]])  # img[height,width]，左上角是原点
        verticalImg.append(img[0:height, segList[i * 2]:segList[i * 2 + 1]])

    return verticalImg


def cfs(img, filename):
    height, width = img.shape
    visited = set()  # 创建一个无序不重复元素集
    q = queue.Queue()
    offset = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    cuts = []

    for x in range(height):  # 从上到下
        for y in range(width):  # 从左到右

            position = []  # 存放点的位置

            if img[x, y] > 1 and (x, y) not in visited:
                q.put((x, y))
                position.append((x, y))
                visited.add((x, y))

            while not q.empty():
                x_p, y_p = q.get()  # get() 第一个元素出队列，并且把值赋值给 x_p，y_p

                for x_offset, y_offset in offset:
                    x_c, y_c = x_p + x_offset, y_p + y_offset

                    if x_c < 0 or y_c < 0 or x_c >= height or y_c >= width:
                        continue

                    if (x_c, y_c) in visited:
                        continue  # 跳出本次循环

                    visited.add((x_c, y_c))

                    # 处理数组越界
                    try:
                        if img[x_c, y_c] > 1:
                            q.put((x_c, y_c))
                            position.append((x_c, y_c))

                    except:
                        pass

            if position:

                sort = sorted(position, key=lambda x: x[1])
                min_y, max_y = sort[0][1], sort[len(sort) - 1][1]
                if max_y - min_y > 30:
                    # 宽度小于30的认为是噪点，根据需要修改
                    cuts.append(position)

    for i in range(len(cuts)):
        cuts[i].insert(0, sorted(cuts[i], key=lambda x: x[1])[0][1])

    cuts_sort = sorted(cuts, key=lambda x: x[0])

    for i in range(len(cuts_sort)):
        del cuts_sort[i][0]

    cfsImg = []
    for i in range(len(cuts_sort)):

        sort_x = sorted(cuts_sort[i], key=lambda x: x[0])
        sort_y = sorted(cuts_sort[i], key=lambda x: x[1])

        cuts_height = sort_x[len(sort_x) - 1][0] - sort_x[0][0]
        cuts_width = sort_y[len(sort_y) - 1][1] - sort_y[0][1]
        panel = np.zeros((cuts_height, cuts_width), dtype=np.uint8)
        for j in range(len(cuts_sort[i])):
            panel[cuts_sort[i][j][0] - sort_x[0][0] - 1, cuts_sort[i][j][1] - sort_y[0][1] - 1] = 255

        blurImg = cv2.medianBlur(panel, 5)  # 新生成的图片会有毛刺，原因尚不清楚

        # cv2.imwrite(r"{}\the {} 's {} character.jpg".format(r"C:\Users\Administrator\Desktop", filename, i), blurImg)
        cfsImg.append(blurImg)

    return cfsImg


def close(img):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
    closed = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

    return closed


def imageProcessing(fileName):
    n = 1  # 递归次数

    x = []
    for i in range(len(fileName)):
        if fileName[i] == '/':
            x.append(i)

    path = fileName[0:max(x)]
    name = fileName[max(x) + 1:len(fileName)]

    img = cv2.imread(r"{}/{}".format(path, name), cv2.IMREAD_GRAYSCALE)  # 1、读取图片文件(灰度)

    scharrImg = scharr(img)  # 2、画出图像的轮廓（scharr算子）

    while True:

        OTSUImg, threshold = recursionOTSU(scharrImg, n)  # 3、区分背景和前景（递归OTSU算法）

        _, binaryImg = cv2.threshold(OTSUImg, threshold, 255, cv2.THRESH_BINARY)  # 4、将前景变为纯白色-像素255（二进制阈值化）

        blurImg = cv2.medianBlur(binaryImg, 3)  # 5、去除噪点（中值滤波，核大小为3）

        hist = cv2.calcHist([blurImg], [0], None, [256], [0, 256])  # 算出前景色占整幅图的百分比，确定是否需要再次递归

        percent = hist[255] / blurImg.size

        if percent < 0.12:  # 如果小于0.117[经过批处理几百张图片，发现凡是大于0.12的图片都是有问题的]，则跳出循环

            break

        n += 1

        print(name, n, percent)

    closeImg = close(blurImg)  # 6、将点连成线（MORPH_CLOSE）

    horizontalImg = horizontalCut(closeImg)  # 7、 横向切割
    # cv2.imshow("img", img)
    # cv2.imshow("scharrImg", scharrImg)
    # cv2.imshow("binaryImg", binaryImg)
    # cv2.imshow("blur", blurImg)
    # cv2.imshow("close", closeImg)
    # cv2.imshow("horizontalImg", horizontalImg)
    #
    # cv2.waitKey()  # 窗口等待
    # cv2.destroyAllWindows()  # 从内存中释放
    # cv2.imwrite(r"C:/Users/Administrator/Desktop/110.jpg", horizontalImg)

    verticalImg = verticalCut(horizontalImg, name, path)  # 8、纵向切割

    global RGB, STATE

    STATE = True
    if len(verticalImg) == 6:

        RGB = [cv2.cvtColor(verticalImg[0], cv2.COLOR_GRAY2BGR), cv2.cvtColor(verticalImg[1], cv2.COLOR_GRAY2BGR),
               cv2.cvtColor(verticalImg[2], cv2.COLOR_GRAY2BGR), cv2.cvtColor(verticalImg[3], cv2.COLOR_GRAY2BGR),
               cv2.cvtColor(verticalImg[4], cv2.COLOR_GRAY2BGR), cv2.cvtColor(verticalImg[5], cv2.COLOR_GRAY2BGR)]

    elif len(verticalImg) == 5:
        try:
            RGB, STATE = drop(verticalImg)
        except:
            STATE = False
            print("{} 滴水算法分割失败".format(name))
    else:

        cfsImg = cfs(horizontalImg, name)

        if len(cfsImg) == 6:

            RGB = [cv2.cvtColor(cfsImg[0], cv2.COLOR_GRAY2BGR), cv2.cvtColor(cfsImg[1], cv2.COLOR_GRAY2BGR),
                   cv2.cvtColor(cfsImg[2], cv2.COLOR_GRAY2BGR), cv2.cvtColor(cfsImg[3], cv2.COLOR_GRAY2BGR),
                   cv2.cvtColor(cfsImg[4], cv2.COLOR_GRAY2BGR), cv2.cvtColor(cfsImg[5], cv2.COLOR_GRAY2BGR)]

        elif len(cfsImg) < 6:

            try:
                RGB[0:6], STATE = drop(cfsImg)
            except:
                STATE = False
                print("{} 滴水算法分割失败".format(name))
        else:
            STATE = False
            print("{} 连通域算法分割多于6块".format(name))

    return RGB, STATE


def drop(adhensionImg):
    global STATE
    STATE = True
    for i in range(len(adhensionImg)):
        height, width = adhensionImg[i].shape
        if width > 115:
            index = i
            adjoin_part = adhensionImg[i]

    dropImg = drop_cut(adjoin_part)
    cv2.imwrite(r"C:/Users/Administrator/Desktop/adhensionImg.jpg", adjoin_part)

    if len(dropImg) == 2:
        if index >= 1:  # 粘连部分在中间
            for i in range(index):
                RGB[i] = cv2.cvtColor(adhensionImg[i], cv2.COLOR_GRAY2BGR)

        RGB[index] = cv2.cvtColor(dropImg[0], cv2.COLOR_GRAY2BGR)
        RGB[index + 1] = cv2.cvtColor(dropImg[1], cv2.COLOR_GRAY2BGR)

        if index + 2 <= 5:  # 粘连部分不是最后
            for j in reversed(range(index + 2, 6)):
                RGB[j] = cv2.cvtColor(adhensionImg[j - 1], cv2.COLOR_GRAY2BGR)
    else:
        STATE = False

    return RGB, STATE


def batchProcess(dir_path):
    sucess = 0
    fail = 0
    starttime = datetime.datetime.now()
    for filename in os.listdir(dir_path):

        pathAndName = "{}/{}".format(dir_path, filename)

        img, STATE = imageProcessing(pathAndName)
        if STATE == True:
            index = filename.index(".")
            filenameNoSuffix = filename[0:index]
            os.makedirs(r"{}/{}".format(dir_path, filenameNoSuffix))
            sucess += 1
            for i in range(6):
                cv2.imwrite(r"{}/{}/{}.jpg".format(dir_path, filenameNoSuffix, i), img[i])
        else:
            fail += 1
    endtime = datetime.datetime.now()
    time = (endtime - starttime).seconds
    print("suceess :", sucess)
    print("fail :", fail)
    return sucess, fail, time


if __name__ == '__main__':
    imageProcessing("C:/Users/Administrator/Desktop/1803.jpg")
    # batchProcess(r"C:/Users/Administrator/Desktop/now")
