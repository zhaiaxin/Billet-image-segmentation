# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1510, 982)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_0 = QtWidgets.QLabel(self.centralwidget)
        self.label_0.setGeometry(QtCore.QRect(230, 80, 1111, 181))
        self.label_0.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label_0.setObjectName("label_0")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(230, 620, 1061, 101))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnOpen = QtWidgets.QPushButton(self.layoutWidget)
        self.btnOpen.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.btnOpen.setObjectName("btnOpen")
        self.horizontalLayout.addWidget(self.btnOpen)
        self.btnProcess = QtWidgets.QPushButton(self.layoutWidget)
        self.btnProcess.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.btnProcess.setObjectName("btnProcess")
        self.horizontalLayout.addWidget(self.btnProcess)
        self.btnSave = QtWidgets.QPushButton(self.layoutWidget)
        self.btnSave.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.btnSave.setObjectName("btnSave")
        self.horizontalLayout.addWidget(self.btnSave)
        self.btnBatch = QtWidgets.QPushButton(self.layoutWidget)
        self.btnBatch.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.btnBatch.setObjectName("btnBatch")
        self.horizontalLayout.addWidget(self.btnBatch)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(600, 290, 181, 231))
        self.label_3.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label_3.setObjectName("label_3")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(980, 290, 181, 231))
        self.label_5.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label_5.setObjectName("label_5")
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(220, 290, 181, 231))
        self.label_1.setStyleSheet("\n"
"background-color: rgb(255, 255, 255);")
        self.label_1.setObjectName("label_1")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(410, 290, 181, 231))
        self.label_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label_2.setObjectName("label_2")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(790, 290, 181, 231))
        self.label_4.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label_4.setObjectName("label_4")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(1170, 290, 181, 231))
        self.label_6.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label_6.setObjectName("label_6")
        self.state = QtWidgets.QLabel(self.centralwidget)
        self.state.setGeometry(QtCore.QRect(480, 560, 601, 31))
        self.state.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.state.setObjectName("state")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_0.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">目标图像</p></body></html>"))
        self.btnOpen.setText(_translate("MainWindow", "打开"))
        self.btnProcess.setText(_translate("MainWindow", "处理"))
        self.btnSave.setText(_translate("MainWindow", "保存"))
        self.btnBatch.setText(_translate("MainWindow", "批处理"))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">第3部分</p></body></html>"))
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">第5部分</p></body></html>"))
        self.label_1.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">第1部分</p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">第2部分</p></body></html>"))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">第4部分</p></body></html>"))
        self.label_6.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">第6部分</p></body></html>"))
        self.state.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">状态</p></body></html>"))

