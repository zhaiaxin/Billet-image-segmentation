import cv2
import numpy as np


temp = [0, 0, 0]

''' 图像竖直投影的长度 '''


def vertical_project(img):
    pix = list(np.sum(np.array(img), axis=0))  # pix存储每一列像素的和
    nonZero = []  # 列表保存像素累加值大于0的列
    for i in range(len(pix)):  # len(pix)代表总共有多少列，也就是图像的宽度
        if pix[i] > 0:
            nonZero.append(i)  # 加入一个对象
    mid = (min(nonZero) + max(nonZero)) // 3  # 返回竖直投影长度的1/3处在原图像的位置
    return mid


''' 确定初始滴落点的位置 img[height,width] '''


def start_point(img, mid):
    height, width = img.shape
    flag = False  # 用来跳出循环 break
    for i in range(height//8,height):  # 防止因为图像顶端的毛刺引起切割错误
        for j in range(mid,width):
            if img[i, j - 1] == 255 and img[i, j] == 0:  # 找到黑白的临界像素
                origin = j
                while (img[i, j] == 0 and j < width-1):
                    j += 1
                differ = j - origin
                if (differ > 0):  # 1000*01中黑像素的个数小于25
                    # print(i, origin)
                    flag = True
                    break  # 跳出第一个 for 循环
        if (flag == True):
            break  # 跳出第二个 for 循环
    return i, origin


'''滴落的规则'''


def drop_rule(img, i, j):
    rule = 1

    left = img[i, j - 1]
    right = img[i, j + 1]
    down = img[i + 1, j]
    bottomLeft = img[i + 1, j - 1]
    bottomRight = img[i + 1, j + 1]
    location = [bottomLeft, down, bottomRight, right, left]

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


'''滴落动作，n用来记录次数'''


def drop_action(rule, i, j, n):
    global temp

    if n % 3 == 1:
        temp[0] = rule
    elif n % 3 == 2:
        temp[1] = rule
    elif n % 3 == 0:
        temp[2] = rule

    '''当水滴左右循环移动时，让其下滴落'''
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


''' 滴落的路径 '''


def drop_way(img, i, j):
    way = []
    n = 1
    height, width = img.shape
    while i in range(height - 1) and j in range(width - 1):
        rule = drop_rule(img, i, j)  # 2、滴落的规则
        i, j = drop_action(rule, i, j, n)  # 3、滴落的动作
        n += 1
        way.append((i, j))
    return way


''' 实行切割 '''


def drop_split(img, way):
    height, width = img.shape
    way.sort(key=lambda x: x[1])  # 根据宽度对切割路径进行排序
    minimum = way[0][1]
    maximum = way[len(way) - 1][1]
    leftImg = img[0:height, 0:maximum]
    rightImg = img
    for i in range(len(way)):
        y = way[i][0]
        x = way[i][1]
        img[y][x-5:x] = 128
        img[y][x:x+5] = 128
    #
    #     for j in range(maximum - x):
    #         b = x + j
    #         leftImg[y, x + j] = 0
    #     for k in range(x - minimum):
    #         a = x - k
    #         rightImg[y, x - k] = 0
    rightImg = img[0:height, minimum:width]

    return leftImg, rightImg

def drop_cut(img):
    mid = vertical_project(img)  # 1、确定起点
    i, j = start_point(img, mid)
    way = drop_way(img, i, j)
    leftImg, rightImg = drop_split(img, way)  # 4、进行切割
    return leftImg, rightImg

if __name__ == '__main__':
    img = cv2.imread(r"C:\Users\Administrator\Desktop\adhensionImg.jpg", cv2.IMREAD_GRAYSCALE)

    leftImg, rightImg = drop_cut(img)
    #
    cv2.imwrite(r"C:\Users\Administrator\Desktop\leftImg.jpg", leftImg)
    cv2.imwrite(r"C:\Users\Administrator\Desktop\rightImg.jpg", rightImg)
    cv2.imwrite(r"C:\Users\Administrator\Desktop\img.jpg", img)

