# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import os

folder_main= os.getcwd().replace("/functions", "")
folder_img = os.path.join(folder_main, "img")
img_math = folder_img + "/math.png"
img_logo = folder_img + "/bulle-de-chat.png"

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(815, 638)
        MainWindow.setStyleSheet("QMainWindow {\n"
"    background-color: white;\n"
"}\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.list_forum = QtWidgets.QLabel(self.centralwidget)
        self.list_forum.setGeometry(QtCore.QRect(40, 100, 141, 16))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.list_forum.setFont(font)
        self.list_forum.setStyleSheet("QLabel#list_forum {\n"
"font-size: 18px;\n"
"font-weigh: bold;\n"
"}")
        self.list_forum.setObjectName("list_forum")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(10, 130, 771, 421))
        self.frame.setStyleSheet("QFrame#item_forums, #item_forums_2, #item_forums_3, #item_forums_4 {\n"
"border: 1px solid rgba(232, 232, 232, 200);\n"
"background-color: #fafafa;\n"
"}\n"
"\n"
"QFrame#frame {\n"
"border: 0px;\n"
"}\n"
"")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.item_forums = QtWidgets.QFrame(self.frame)
        self.item_forums.setGeometry(QtCore.QRect(20, 40, 351, 161))
        self.item_forums.setStyleSheet("QLabel#title {\n"
"font-size: 18px;\n"
"}")
        self.item_forums.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.item_forums.setFrameShadow(QtWidgets.QFrame.Raised)
        self.item_forums.setObjectName("item_forums")
        self.logo_math = QtWidgets.QLabel(self.item_forums)
        self.logo_math.setGeometry(QtCore.QRect(10, 10, 71, 71))
        self.logo_math.setText("")
        self.logo_math.setPixmap(QtGui.QPixmap(img_math))
        self.logo_math.setScaledContents(True)
        self.logo_math.setObjectName("logo_math")
        self.title = QtWidgets.QLabel(self.item_forums)
        self.title.setGeometry(QtCore.QRect(110, 10, 121, 31))
        self.title.setStyleSheet("QLabel#list_forum {\n"
"font-size: 18px;\n"
"font-weigh: bold;\n"
"}")
        self.title.setObjectName("title")
        self.label = QtWidgets.QLabel(self.item_forums)
        self.label.setGeometry(QtCore.QRect(110, 40, 231, 16))
        self.label.setObjectName("label")
        self.title_2 = QtWidgets.QLabel(self.item_forums)
        self.title_2.setGeometry(QtCore.QRect(10, 90, 121, 31))
        self.title_2.setStyleSheet("QLabel#list_forum {\n"
"font-size: 18px;\n"
"font-weigh: bold;\n"
"}")
        self.title_2.setObjectName("title_2")
        self.label_3 = QtWidgets.QLabel(self.item_forums)
        self.label_3.setGeometry(QtCore.QRect(10, 130, 91, 16))
        self.label_3.setObjectName("label_3")
        self.verticalScrollBar = QtWidgets.QScrollBar(self.frame)
        self.verticalScrollBar.setGeometry(QtCore.QRect(750, 0, 21, 418))
        self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar.setObjectName("verticalScrollBar")
        self.item_forums_2 = QtWidgets.QFrame(self.frame)
        self.item_forums_2.setGeometry(QtCore.QRect(380, 40, 351, 161))
        self.item_forums_2.setStyleSheet("QLabel#title_3 {\n"
"font-size: 18px;\n"
"}")
        self.item_forums_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.item_forums_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.item_forums_2.setObjectName("item_forums_2")
        self.title_3 = QtWidgets.QLabel(self.item_forums_2)
        self.title_3.setGeometry(QtCore.QRect(110, 10, 111, 31))
        self.title_3.setStyleSheet("QLabel#list_forum {\n"
"font-size: 18px;\n"
"font-weigh: bold;\n"
"}")
        self.title_3.setObjectName("title_3")
        self.label_1 = QtWidgets.QLabel(self.item_forums_2)
        self.label_1.setGeometry(QtCore.QRect(110, 40, 231, 16))
        self.label_1.setObjectName("label_1")
        self.title_4 = QtWidgets.QLabel(self.item_forums_2)
        self.title_4.setGeometry(QtCore.QRect(10, 90, 121, 31))
        self.title_4.setStyleSheet("QLabel#list_forum {\n"
"font-size: 18px;\n"
"font-weigh: bold;\n"
"}")
        self.title_4.setObjectName("title_4")
        self.label_2 = QtWidgets.QLabel(self.item_forums_2)
        self.label_2.setGeometry(QtCore.QRect(10, 130, 91, 16))
        self.label_2.setObjectName("label_2")
        self.logo_math_3 = QtWidgets.QLabel(self.item_forums_2)
        self.logo_math_3.setGeometry(QtCore.QRect(10, 10, 71, 71))
        self.logo_math_3.setText("")
        self.logo_math_3.setPixmap(QtGui.QPixmap("../img/math.png"))
        self.logo_math_3.setScaledContents(True)
        self.logo_math_3.setObjectName("logo_math_3")
        self.item_forums_3 = QtWidgets.QFrame(self.frame)
        self.item_forums_3.setGeometry(QtCore.QRect(380, 250, 351, 161))
        self.item_forums_3.setStyleSheet("QLabel#title_9 {\n"
"font-size: 18px;\n"
"}")
        self.item_forums_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.item_forums_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.item_forums_3.setObjectName("item_forums_3")
        self.title_9 = QtWidgets.QLabel(self.item_forums_3)
        self.title_9.setGeometry(QtCore.QRect(110, 10, 91, 31))
        self.title_9.setStyleSheet("QLabel#list_forum {\n"
"font-size: 18px;\n"
"font-weigh: bold;\n"
"}")
        self.title_9.setObjectName("title_9")
        self.label_9 = QtWidgets.QLabel(self.item_forums_3)
        self.label_9.setGeometry(QtCore.QRect(110, 40, 231, 16))
        self.label_9.setObjectName("label_9")
        self.title_10 = QtWidgets.QLabel(self.item_forums_3)
        self.title_10.setGeometry(QtCore.QRect(10, 90, 121, 31))
        self.title_10.setStyleSheet("QLabel#list_forum {\n"
"font-size: 18px;\n"
"font-weigh: bold;\n"
"}")
        self.title_10.setObjectName("title_10")
        self.label_10 = QtWidgets.QLabel(self.item_forums_3)
        self.label_10.setGeometry(QtCore.QRect(10, 130, 91, 16))
        self.label_10.setObjectName("label_10")
        self.logo_math_4 = QtWidgets.QLabel(self.item_forums_3)
        self.logo_math_4.setGeometry(QtCore.QRect(20, 10, 71, 71))
        self.logo_math_4.setText("")
        self.logo_math_4.setPixmap(QtGui.QPixmap("../img/math.png"))
        self.logo_math_4.setScaledContents(True)
        self.logo_math_4.setObjectName("logo_math_4")
        self.item_forums_4 = QtWidgets.QFrame(self.frame)
        self.item_forums_4.setGeometry(QtCore.QRect(20, 253, 351, 161))
        self.item_forums_4.setStyleSheet("QLabel#title, #title_11 {\n"
"font-size: 18px;\n"
"}")
        self.item_forums_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.item_forums_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.item_forums_4.setObjectName("item_forums_4")
        self.title_11 = QtWidgets.QLabel(self.item_forums_4)
        self.title_11.setGeometry(QtCore.QRect(110, 10, 81, 31))
        self.title_11.setStyleSheet("QLabel#list_forum {\n"
"font-size: 18px;\n"
"font-weigh: bold;\n"
"}")
        self.title_11.setObjectName("title_11")
        self.label_11 = QtWidgets.QLabel(self.item_forums_4)
        self.label_11.setGeometry(QtCore.QRect(110, 40, 231, 16))
        self.label_11.setObjectName("label_11")
        self.title_12 = QtWidgets.QLabel(self.item_forums_4)
        self.title_12.setGeometry(QtCore.QRect(10, 90, 121, 31))
        self.title_12.setStyleSheet("QLabel#list_forum {\n"
"font-size: 18px;\n"
"font-weigh: bold;\n"
"}")
        self.title_12.setObjectName("title_12")
        self.label_12 = QtWidgets.QLabel(self.item_forums_4)
        self.label_12.setGeometry(QtCore.QRect(10, 130, 91, 16))
        self.label_12.setObjectName("label_12")
        self.logo_math_5 = QtWidgets.QLabel(self.item_forums_4)
        self.logo_math_5.setGeometry(QtCore.QRect(10, 10, 71, 71))
        self.logo_math_5.setText("")
        self.logo_math_5.setPixmap(QtGui.QPixmap("../img/math.png"))
        self.logo_math_5.setScaledContents(True)
        self.logo_math_5.setObjectName("logo_math_5")
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setGeometry(QtCore.QRect(30, 220, 131, 16))
        self.label_4.setStyleSheet("font-size: 18px;")
        self.label_4.setObjectName("label_4")
        self.label_13 = QtWidgets.QLabel(self.frame)
        self.label_13.setGeometry(QtCore.QRect(30, 10, 161, 16))
        self.label_13.setStyleSheet("font-size: 18px;")
        self.label_13.setObjectName("label_13")
        self.nav_bar = QtWidgets.QFrame(self.centralwidget)
        self.nav_bar.setGeometry(QtCore.QRect(14, 10, 731, 61))
        self.nav_bar.setStyleSheet("QFrame#nav_bar {\n"
"border:1px solid black; \n"
"border-left: 0px;\n"
"border-right: 0px;\n"
"border-top: 0px;\n"
"}\n"
"\n"
"QLabel#logo{\n"
"    font-size: 24px;\n"
"}\n"
"")
        self.nav_bar.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.nav_bar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.nav_bar.setObjectName("nav_bar")
        self.label_5 = QtWidgets.QLabel(self.nav_bar)
        self.label_5.setGeometry(QtCore.QRect(10, 0, 60, 51))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap(img_logo))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(610, 20, 131, 41))
        self.pushButton.setStyleSheet("QPushButton#pushButton {\n"
"color: blue;\n"
"border: 1px solid blue;\n"
"border-radius: 5px;\n"
"padding: 10px;\n"
"font-size: 18px;\n"
"}\n"
"\n"
"QPushButton#pushButton::hover {\n"
"color: white;\n"
"background-color: blue;\n"
"}")
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 815, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.list_forum.setText(_translate("MainWindow", "Liste des forums"))
        self.title.setText(_translate("MainWindow", "Mathematique"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-family:\'Montserrat,sans-serif\'; font-size:14px; color:#565656; vertical-align:top;\">Vos questions à propos des math.</span></p></body></html>"))
        self.title_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt; text-decoration: underline;\">Dernier sujet:</span></p></body></html>"))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-family:\'Montserrat,sans-serif\'; font-size:14px; color:#565656; vertical-align:top;\">Unité mesure</span></p></body></html>"))
        self.title_3.setText(_translate("MainWindow", "Physique"))
        self.label_1.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-family:\'Montserrat,sans-serif\'; font-size:14px; color:#565656; vertical-align:top;\">Vos questions à propos des math.</span></p></body></html>"))
        self.title_4.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt; text-decoration: underline;\">Dernier sujet:</span></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-family:\'Montserrat,sans-serif\'; font-size:14px; color:#565656; vertical-align:top;\">Unité mesure</span></p></body></html>"))
        self.title_9.setText(_translate("MainWindow", "Philo"))
        self.label_9.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-family:\'Montserrat,sans-serif\'; font-size:14px; color:#565656; vertical-align:top;\">Vos questions à propos des math.</span></p></body></html>"))
        self.title_10.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt; text-decoration: underline;\">Dernier sujet:</span></p></body></html>"))
        self.label_10.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-family:\'Montserrat,sans-serif\'; font-size:14px; color:#565656; vertical-align:top;\">Unité mesure</span></p></body></html>"))
        self.title_11.setText(_translate("MainWindow", "Français"))
        self.label_11.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-family:\'Montserrat,sans-serif\'; font-size:14px; color:#565656; vertical-align:top;\">Vos questions à propos des math.</span></p></body></html>"))
        self.title_12.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt; text-decoration: underline;\">Dernier sujet:</span></p></body></html>"))
        self.label_12.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-family:\'Montserrat,sans-serif\'; font-size:14px; color:#565656; vertical-align:top;\">Unité mesure</span></p></body></html>"))
        self.label_4.setText(_translate("MainWindow", "Matiére litéraire"))
        self.label_13.setText(_translate("MainWindow", "Matiere scientifique"))
        self.pushButton.setText(_translate("MainWindow", "Se connecter"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
