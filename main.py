#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import cv2
import numpy as np

from PyQt5 import QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

from gui.gui import Ui_MainWindow
from process import image_process, batch_process
from util.split import split_dot, split_slash

PATH_NAME_SUFFIX = ''
STATE = True


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)

        # Initializes an img object of type ndarray and assigns an initial value
        self.img = [np.zeros(()), np.zeros(()), np.zeros(()),
                    np.zeros(()), np.zeros(()), np.zeros(()),
                    np.zeros(())]

        self.btnOpen.clicked.connect(self.open_slot)
        self.btnSave.clicked.connect(self.save_slot)
        self.btnProcess.clicked.connect(self.process_slot)
        self.btnBatch.clicked.connect(self.batch_process_slot)

    def open_slot(self):

        global PATH_NAME_SUFFIX
        PATH_NAME_SUFFIX, tmp = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Open Image', './__data', '*.png *.jpg *.bmp')

        if PATH_NAME_SUFFIX is '':
            return

        #  img[0] represent the source image
        self.img[0] = cv2.imread(PATH_NAME_SUFFIX)

        if self.img[0].size == 1:
            return

        self.refresh_show()

    def save_slot(self):

        PATH_NAME_SUFFIX, tmp = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save Image', './__data', '*.png *.jpg *.bmp', '*.jpg')

        if PATH_NAME_SUFFIX is '':
            return
        if self.img[0].size == 1:
            return

        path, name_suffix = split_slash(PATH_NAME_SUFFIX)
        name = split_dot(name_suffix)

        #  write all data of img list to the path
        for i in range(len(self.img) - 1):
            cv2.imwrite(r"{}/{}'s {} part.jpg".format(path, name, i), self.img[i])

    def process_slot(self):
        if self.img[0].size == 1:
            return

        global STATE
        STATE = True

        self.img[1:7], STATE = image_process(PATH_NAME_SUFFIX)
        self.refresh_show()

    def refresh_show(self):

        if STATE == False:
            print("error")
        else:

            for i in range(len(self.img)):

                if np.sum(self.img[i]) == 0:
                    break
                height, width, channel = self.img[i].shape
                img = cv2.cvtColor(self.img[i], cv2.COLOR_BGR2RGB)
                QIm = QImage(img.data, width, height,
                             width * channel,
                             QImage.Format_RGB888)

                if i == 0:
                    self.label_0.setPixmap(QPixmap.fromImage(QIm))
                    self.label_0.setAlignment(Qt.AlignCenter)
                elif i == 1:
                    self.label_1.setPixmap(QPixmap.fromImage(QIm))
                    self.label_1.setAlignment(Qt.AlignCenter)
                elif i == 2:
                    self.label_2.setPixmap(QPixmap.fromImage(QIm))
                    self.label_2.setAlignment(Qt.AlignCenter)
                elif i == 3:
                    self.label_3.setPixmap(QPixmap.fromImage(QIm))
                    self.label_3.setAlignment(Qt.AlignCenter)
                elif i == 4:
                    self.label_4.setPixmap(QPixmap.fromImage(QIm))
                    self.label_4.setAlignment(Qt.AlignCenter)
                elif i == 5:
                    self.label_5.setPixmap(QPixmap.fromImage(QIm))
                    self.label_5.setAlignment(Qt.AlignCenter)
                elif i == 6:
                    self.label_6.setPixmap(QPixmap.fromImage(QIm))
                    self.label_6.setAlignment(Qt.AlignCenter)

    def batch_process_slot(self):

        self.cwd = os.getcwd()
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select folder", self.cwd)

        if path is '':
            return

        success, fail, time = batch_process(path)
        self.refresh_state(success, fail, time)

    def refresh_state(self, success, fail, time):
        self.state.setText("成功：{}个  失败：{} 个  总用时: {}秒".format(success, fail, time))
        self.state.setAlignment(Qt.AlignCenter)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
