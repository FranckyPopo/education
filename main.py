# -*- coding: utf-8 -*-

import os
import sqlite3
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

# Nous créons le dossier qui va cotenir les bd
folder_current = os.getcwd()
folder_bd = os.path.join(folder_current, "data")
os.makedirs(folder_bd, exist_ok="yes")

class Frame(QtWidgets.QFrame):
    clicked = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        QtWidgets.QFrame.__init__(self, parent=parent)

    def mousePressEvent(self, event):
        self.clicked.emit()


class Ui_MainWindow(object):
    def window_connection(self):
        self.stackedWidget.setCurrentWidget(self.page_connection)
        
    def window_subscription(self):
        self.stackedWidget.setCurrentWidget(self.page_subscription)

         
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1021, 703)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(310, 0, 711, 671))
        self.stackedWidget.setStyleSheet("")
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_discuss = QtWidgets.QWidget()
        self.page_discuss.setObjectName("page_discuss")
        self.contenai_discuss = QtWidgets.QScrollArea(self.page_discuss)
        self.contenai_discuss.setGeometry(QtCore.QRect(0, 0, 755, 671))
        self.contenai_discuss.setStyleSheet("QScrollArea#contenai_discuss {\n"
"border: 0px;\n"
"}\n"
"\n"
"QWidget#discuss{\n"
"background-color: rgb(255, 255, 255);\n"
"\n"
"}")
        self.contenai_discuss.setWidgetResizable(True)
        self.contenai_discuss.setObjectName("contenai_discuss")
        self.discuss = QtWidgets.QWidget()
        self.discuss.setGeometry(QtCore.QRect(0, 0, 755, 671))
        self.discuss.setObjectName("discuss")
        self.contenai_discuss.setWidget(self.discuss)
        self.stackedWidget.addWidget(self.page_discuss)
        self.page_subjet = QtWidgets.QWidget()
        self.page_subjet.setObjectName("page_subjet")
        self.contenai_subjet = QtWidgets.QScrollArea(self.page_subjet)
        self.contenai_subjet.setGeometry(QtCore.QRect(0, 0, 831, 671))
        self.contenai_subjet.setStyleSheet("QScrollArea#contenai_subjet {\n"
"border: 0px;\n"
"}\n"
"\n"
"QWidget#subjet{\n"
"background-color: rgb(255, 255, 255);\n"
"\n"
"}")
        self.contenai_subjet.setWidgetResizable(True)
        self.contenai_subjet.setObjectName("contenai_subjet")
        self.subjet = QtWidgets.QWidget()
        self.subjet.setGeometry(QtCore.QRect(0, 0, 831, 671))
        self.subjet.setObjectName("subjet")
        self.contenai_subjet.setWidget(self.subjet)
        self.stackedWidget.addWidget(self.page_subjet)
        self.page_connection = QtWidgets.QWidget()
        self.page_connection.setObjectName("page_connection")
        self.frame_connection = QtWidgets.QFrame(self.page_connection)
        self.frame_connection.setGeometry(QtCore.QRect(-10, 0, 725, 691))
        self.frame_connection.setStyleSheet("QFrame#frame_connection{\n"
"background-color: rgb(255, 255, 255);\n"
"}")
        self.frame_connection.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_connection.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_connection.setObjectName("frame_connection")
        self.enter_email_connection = QtWidgets.QLineEdit(self.frame_connection)
        self.enter_email_connection.setGeometry(QtCore.QRect(230, 289, 331, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.enter_email_connection.setFont(font)
        self.enter_email_connection.setStyleSheet("QLineEdit#enter_email_connection{\n"
"background-color: rgb(236, 236, 236);\n"
"padding: 5px;\n"
"border: 1px solid rgb(160, 161, 182);\n"
"border-left: 0px;\n"
"border-right: 0px;\n"
"border-top: 0px;\n"
"}\n"
"\n"
"QLineEdit#enter_email_connection::hover {\n"
"border-bottom-color:  rgb(64, 40, 200);\n"
"}")
        self.enter_email_connection.setObjectName("enter_email_connection")
        self.label_connection_2 = QtWidgets.QLabel(self.frame_connection)
        self.label_connection_2.setGeometry(QtCore.QRect(300, 210, 181, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label_connection_2.setFont(font)
        self.label_connection_2.setObjectName("label_connection_2")
        self.enter_password_connection = QtWidgets.QLineEdit(self.frame_connection)
        self.enter_password_connection.setGeometry(QtCore.QRect(230, 340, 331, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.enter_password_connection.setFont(font)
        self.enter_password_connection.setStyleSheet("QLineEdit#enter_password_connection{\n"
"background-color: rgb(236, 236, 236);\n"
"padding: 5px;\n"
"border: 1px solid rgb(160, 161, 182);\n"
"border-left: 0px;\n"
"border-right: 0px;\n"
"border-top: 0px;\n"
"}\n"
"\n"
"QLineEdit#enter_password_connection::hover {\n"
"border-bottom-color: rgb(64, 40, 200);\n"
"\n"
"}")
        self.enter_password_connection.setObjectName("enter_password_connection")
        self.bnt_connection = QtWidgets.QPushButton(self.frame_connection)
        self.bnt_connection.setGeometry(QtCore.QRect(298, 400, 211, 31))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(14)
        self.bnt_connection.setFont(font)
        self.bnt_connection.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bnt_connection.setStyleSheet("QPushButton#bnt_connection{\n"
"background-color: white;\n"
"color: rgb(64, 40, 200);\n"
"padding: 5px;\n"
"border: 2px solid rgb(64, 40, 200);\n"
"border-radius: 5px;\n"
"}\n"
"\n"
"\n"
"QPushButton#bnt_connection::hover{\n"
"background-color: rgb(64, 40, 200);\n"
"color: white;\n"
"}\n"
"")
        self.bnt_connection.setObjectName("bnt_connection")
        self.lien_subscription = QtWidgets.QPushButton(self.frame_connection)
        self.lien_subscription.clicked.connect(self.window_subscription)
        self.lien_subscription.setGeometry(QtCore.QRect(420, 450, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.lien_subscription.setFont(font)
        self.lien_subscription.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.lien_subscription.setStyleSheet("QPushButton#lien_subscription{\n"
"background-color: rgb(255, 255, 255);\n"
"color:  rgb(64, 40, 200);\n"
"border: 0px;\n"
"}\n"
"\n"
"QPushButton#lien_subscription::hover{\n"
"font-weight: bold;\n"
"}")
        self.lien_subscription.setObjectName("lien_subscription")
        self.label_unitile = QtWidgets.QLabel(self.frame_connection)
        self.label_unitile.setGeometry(QtCore.QRect(230, 458, 201, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.label_unitile.setFont(font)
        self.label_unitile.setObjectName("label_unitile")
        self.stackedWidget.addWidget(self.page_connection)
        self.page_subscription = QtWidgets.QWidget()
        self.page_subscription.setObjectName("page_subscription")
        self.frame_subscribtion = QtWidgets.QFrame(self.page_subscription)
        self.frame_subscribtion.setGeometry(QtCore.QRect(0, 0, 714, 672))
        self.frame_subscribtion.setStyleSheet("QFrame#frame_subscribtion{\n"
"background-color: rgb(255, 255, 255);\n"
"}")
        self.frame_subscribtion.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_subscribtion.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_subscribtion.setObjectName("frame_subscribtion")
        self.enter_email = QtWidgets.QLineEdit(self.frame_subscribtion)
        self.enter_email.setGeometry(QtCore.QRect(226, 269, 331, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.enter_email.setFont(font)
        self.enter_email.setStyleSheet("QLineEdit#enter_email{\n"
"background-color: rgb(236, 236, 236);\n"
"border-radius: 3px;\n"
"padding: 5px;\n"
"border: 1px solid rgb(160, 161, 182);\n"
"border-left: 0px;\n"
"border-right: 0px;\n"
"border-top: 0px;\n"
"}\n"
"\n"
"QLineEdit#enter_email::hover {\n"
"border-bottom-color:  rgb(64, 40, 200);\n"
"\n"
"}")
        self.enter_email.setObjectName("enter_email")
        self.bnt_subcription = QtWidgets.QPushButton(self.frame_subscribtion)
        self.bnt_subcription.setGeometry(QtCore.QRect(286, 514, 211, 31))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(14)
        self.bnt_subcription.setFont(font)
        self.bnt_subcription.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bnt_subcription.setStyleSheet("QPushButton#bnt_subcription{\n"
"background-color: white;\n"
"color: rgb(64, 40, 200);\n"
"padding: 5px;\n"
"border: 2px solid rgb(64, 40, 200);\n"
"border-radius: 5px;\n"
"}\n"
"\n"
"\n"
"QPushButton#bnt_subcription::hover{\n"
"background-color: rgb(64, 40, 200);\n"
"color: white;\n"
"}\n"
"")
        self.bnt_subcription.setObjectName("bnt_subcription")
        self.enter_last_name = QtWidgets.QLineEdit(self.frame_subscribtion)
        self.enter_last_name.setGeometry(QtCore.QRect(226, 164, 331, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.enter_last_name.setFont(font)
        self.enter_last_name.setStyleSheet("QLineEdit#enter_last_name{\n"
"background-color: rgb(236, 236, 236);\n"
"border-radius: 3px;\n"
"padding: 5px;\n"
"border: 1px solid rgb(160, 161, 182);\n"
"border-left: 0px;\n"
"border-right: 0px;\n"
"border-top: 0px;\n"
"}\n"
"\n"
"QLineEdit#enter_last_name::hover {\n"
"border-bottom-color:  rgb(64, 40, 200);\n"
"\n"
"}")
        self.enter_last_name.setObjectName("enter_last_name")
        self.enter_first_name = QtWidgets.QLineEdit(self.frame_subscribtion)
        self.enter_first_name.setGeometry(QtCore.QRect(226, 218, 331, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.enter_first_name.setFont(font)
        self.enter_first_name.setStyleSheet("QLineEdit#enter_first_name{\n"
"background-color: rgb(236, 236, 236);\n"
"border-radius: 3px;\n"
"padding: 5px;\n"
"border: 1px solid rgb(160, 161, 182);\n"
"border-left: 0px;\n"
"border-right: 0px;\n"
"border-top: 0px;\n"
"}\n"
"\n"
"QLineEdit#enter_first_name::hover {\n"
"border-bottom-color:  rgb(64, 40, 200);\n"
"\n"
"}")
        self.enter_first_name.setObjectName("enter_first_name")
        self.enter_password_2 = QtWidgets.QLineEdit(self.frame_subscribtion)
        self.enter_password_2.setGeometry(QtCore.QRect(226, 457, 331, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.enter_password_2.setFont(font)
        self.enter_password_2.setStyleSheet("QLineEdit#enter_password_2{\n"
"background-color: rgb(236, 236, 236);\n"
"border-radius: 3px;\n"
"padding: 5px;\n"
"border: 1px solid rgb(160, 161, 182);\n"
"border-left: 0px;\n"
"border-right: 0px;\n"
"border-top: 0px;\n"
"}\n"
"\n"
"QLineEdit#enter_password_2::hover {\n"
"border-bottom-color:  rgb(64, 40, 200);\n"
"\n"
"}")
        self.enter_password_2.setObjectName("enter_password_2")
        self.enter_password_1 = QtWidgets.QLineEdit(self.frame_subscribtion)
        self.enter_password_1.setGeometry(QtCore.QRect(226, 410, 331, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.enter_password_1.setFont(font)
        self.enter_password_1.setStyleSheet("QLineEdit#enter_password_1{\n"
"background-color: rgb(236, 236, 236);\n"
"border-radius: 3px;\n"
"padding: 5px;\n"
"border: 1px solid rgb(160, 161, 182);\n"
"border-left: 0px;\n"
"border-right: 0px;\n"
"border-top: 0px;\n"
"}\n"
"\n"
"QLineEdit#enter_password_1::hover {\n"
"border-bottom-color:  rgb(64, 40, 200);\n"
"\n"
"}")
        self.enter_password_1.setObjectName("enter_password_1")
        self.enter_gender = QtWidgets.QComboBox(self.frame_subscribtion)
        self.enter_gender.setGeometry(QtCore.QRect(226, 324, 331, 24))
        self.enter_gender.setStyleSheet("QComboBox#enter_gender {\n"
"border-left: 0px; \n"
"border-top: 0px; \n"
"border-right: 0px;\n"
"border-radius: 3px; \n"
"border-bottom: 1px solid rgb(204, 204, 204); \n"
"background-color: rgb(236, 236, 236);\n"
"}\n"
"\n"
"QComboBox#enter_gender::hover {\n"
"border-bottom-color: rgb(160, 161, 182);\n"
"}\n"
"")
        self.enter_gender.setObjectName("enter_gender")
        self.enter_class = QtWidgets.QComboBox(self.frame_subscribtion)
        self.enter_class.setGeometry(QtCore.QRect(226, 366, 331, 24))
        self.enter_class.setStyleSheet("QComboBox#enter_class {\n"
"border-left: 0px; \n"
"border-top: 0px; \n"
"border-radius: 3px;\n"
"border-right: 0px;\n"
"border-bottom: 1px solid rgb(204, 204, 204); \n"
"background-color: rgb(236, 236, 236);\n"
"}\n"
"\n"
"QComboBox#enter_classr::hover {\n"
"border-bottom-color: rgb(160, 161, 182);\n"
"}\n"
"")
        self.enter_class.setObjectName("enter_class")
        self.label_subscription = QtWidgets.QLabel(self.frame_subscribtion)
        self.label_subscription.setGeometry(QtCore.QRect(300, 84, 171, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label_subscription.setFont(font)
        self.label_subscription.setStyleSheet("")
        self.label_subscription.setObjectName("label_subscription")
        self.lien_connection = QtWidgets.QPushButton(self.frame_subscribtion)
        self.lien_connection.clicked.connect(self.window_connection)
        self.lien_connection.setGeometry(QtCore.QRect(422, 562, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.lien_connection.setFont(font)
        self.lien_connection.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.lien_connection.setStyleSheet("QPushButton#lien_connection{\n"
"background-color: rgb(255, 255, 255);\n"
"color:  rgb(64, 40, 200);\n"
"border: 0px;\n"
"}\n"
"\n"
"QPushButton#lien_connection::hover{\n"
"font-weight: bold;\n"
"}")
        self.lien_connection.setObjectName("lien_connection")
        self.label_unitile_2 = QtWidgets.QLabel(self.frame_subscribtion)
        self.label_unitile_2.setGeometry(QtCore.QRect(229, 570, 201, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.label_unitile_2.setFont(font)
        self.label_unitile_2.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.label_unitile_2.setStyleSheet("")
        self.label_unitile_2.setObjectName("label_unitile_2")
        self.stackedWidget.addWidget(self.page_subscription)
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(0, 0, 311, 671))
        self.scrollArea.setStyleSheet("QScrollArea#scrollArea{\n"
"border: 0px;\n"
"}")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.bar_nav = QtWidgets.QWidget()
        self.bar_nav.setGeometry(QtCore.QRect(0, 0, 311, 671))
        self.bar_nav.setObjectName("bar_nav")
        self.frame_conne_1 = Frame(self.bar_nav)
        self.frame_conne_1.clicked.connect(self.window_connection)
        self.frame_conne_1.setGeometry(QtCore.QRect(10, 572, 311, 80))
        self.frame_conne_1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.frame_conne_1.setStyleSheet("QFrame#frame_conne_1::hover{\n"
"background-color: rgb(204, 204, 204);\n"
"}")
        self.frame_conne_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_conne_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_conne_1.setObjectName("frame_conne_1")
        self.label_connection = QtWidgets.QLabel(self.frame_conne_1)
        self.label_connection.setGeometry(QtCore.QRect(110, 31, 131, 32))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_connection.setFont(font)
        self.label_connection.setObjectName("label_connection")
        self.label_user_connection = QtWidgets.QLabel(self.frame_conne_1)
        self.label_user_connection.setGeometry(QtCore.QRect(16, 10, 71, 70))
        self.label_user_connection.setText("")
        self.label_user_connection.setPixmap(QtGui.QPixmap("UI\\../img/personne.png"))
        self.label_user_connection.setScaledContents(True)
        self.label_user_connection.setObjectName("label_user_connection")
        self.label = QtWidgets.QLabel(self.bar_nav)
        self.label.setGeometry(QtCore.QRect(30, 12, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.label.setObjectName("label")
        self.label_matire_scientifique = QtWidgets.QLabel(self.bar_nav)
        self.label_matire_scientifique.setGeometry(QtCore.QRect(50, 56, 191, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.label_matire_scientifique.setFont(font)
        self.label_matire_scientifique.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.label_matire_scientifique.setObjectName("label_matire_scientifique")
        self.frame_category_4 = QtWidgets.QFrame(self.bar_nav)
        self.frame_category_4.setGeometry(QtCore.QRect(10, 492, 311, 71))
        self.frame_category_4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.frame_category_4.setStyleSheet("QFrame#frame_category_4::hover{\n"
"background-color: rgb(204, 204, 204);\n"
"}")
        self.frame_category_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_category_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_category_4.setObjectName("frame_category_4")
        self.label_9 = QtWidgets.QLabel(self.frame_category_4)
        self.label_9.setGeometry(QtCore.QRect(120, 20, 131, 34))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(16)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.logo_6 = QtWidgets.QLabel(self.frame_category_4)
        self.logo_6.setGeometry(QtCore.QRect(30, 10, 61, 51))
        self.logo_6.setText("")
        self.logo_6.setPixmap(QtGui.QPixmap("UI\\../img/philosophie.png"))
        self.logo_6.setScaledContents(True)
        self.logo_6.setObjectName("logo_6")
        self.frame_category_1 = QtWidgets.QFrame(self.bar_nav)
        self.frame_category_1.setGeometry(QtCore.QRect(10, 238, 311, 61))
        self.frame_category_1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.frame_category_1.setStyleSheet("QFrame#frame_category_1::hover{\n"
"background-color: rgb(204, 204, 204);\n"
"}")
        self.frame_category_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_category_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_category_1.setObjectName("frame_category_1")
        self.label_4 = QtWidgets.QLabel(self.frame_category_1)
        self.label_4.setGeometry(QtCore.QRect(120, 14, 153, 34))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(16)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.logo_3 = QtWidgets.QLabel(self.frame_category_1)
        self.logo_3.setGeometry(QtCore.QRect(30, 5, 61, 51))
        self.logo_3.setText("")
        self.logo_3.setPixmap(QtGui.QPixmap("UI\\../img/mathématiques.png"))
        self.logo_3.setScaledContents(True)
        self.logo_3.setObjectName("logo_3")
        self.frame_category_2 = QtWidgets.QFrame(self.bar_nav)
        self.frame_category_2.setGeometry(QtCore.QRect(10, 171, 311, 61))
        self.frame_category_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.frame_category_2.setStyleSheet("QFrame#frame_category_2::hover{\n"
"background-color: rgb(204, 204, 204);\n"
"}")
        self.frame_category_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_category_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_category_2.setObjectName("frame_category_2")
        self.label_7 = QtWidgets.QLabel(self.frame_category_2)
        self.label_7.setGeometry(QtCore.QRect(120, 10, 111, 34))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(16)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.logo_2 = QtWidgets.QLabel(self.frame_category_2)
        self.logo_2.setGeometry(QtCore.QRect(32, 2, 61, 51))
        self.logo_2.setText("")
        self.logo_2.setPixmap(QtGui.QPixmap("UI\\../img/physique.png"))
        self.logo_2.setScaledContents(True)
        self.logo_2.setObjectName("logo_2")
        self.frame_category_3 = QtWidgets.QFrame(self.bar_nav)
        #self.frame_category_3.clicked.connection(self.)
        self.frame_category_3.setGeometry(QtCore.QRect(10, 102, 311, 61))
        self.frame_category_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.frame_category_3.setStyleSheet("QFrame#frame_category_3::hover{\n"
"background-color: rgb(204, 204, 204);\n"
"}")
        self.frame_category_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_category_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_category_3.setObjectName("frame_category_3")
        self.label_8 = QtWidgets.QLabel(self.frame_category_3)
        self.label_8.setGeometry(QtCore.QRect(120, 10, 71, 34))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(16)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.logo = QtWidgets.QLabel(self.frame_category_3)
        self.logo.setGeometry(QtCore.QRect(30, 5, 61, 51))
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap("UI\\../img/planète-terre.png"))
        self.logo.setScaledContents(True)
        self.logo.setObjectName("logo")
        self.frame_category_5 = QtWidgets.QFrame(self.bar_nav)
        self.frame_category_5.setGeometry(QtCore.QRect(10, 420, 311, 61))
        self.frame_category_5.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.frame_category_5.setStyleSheet("QFrame#frame_category_5::hover{\n"
"background-color: rgb(204, 204, 204);\n"
"}")
        self.frame_category_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_category_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_category_5.setObjectName("frame_category_5")
        self.label_10 = QtWidgets.QLabel(self.frame_category_5)
        self.label_10.setGeometry(QtCore.QRect(120, 14, 102, 34))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(16)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.logo_5 = QtWidgets.QLabel(self.frame_category_5)
        self.logo_5.setGeometry(QtCore.QRect(30, 6, 61, 51))
        self.logo_5.setText("")
        self.logo_5.setPixmap(QtGui.QPixmap("UI\\../img/alphabet.png"))
        self.logo_5.setScaledContents(True)
        self.logo_5.setObjectName("logo_5")
        self.label_matiere_litraire = QtWidgets.QLabel(self.bar_nav)
        self.label_matiere_litraire.setGeometry(QtCore.QRect(50, 305, 151, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.label_matiere_litraire.setFont(font)
        self.label_matiere_litraire.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.label_matiere_litraire.setObjectName("label_matiere_litraire")
        self.frame_category_6 = QtWidgets.QFrame(self.bar_nav)
        self.frame_category_6.setGeometry(QtCore.QRect(10, 350, 311, 61))
        self.frame_category_6.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.frame_category_6.setStyleSheet("QFrame#frame_category_6::hover{\n"
"background-color: rgb(204, 204, 204);\n"
"}")
        self.frame_category_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_category_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_category_6.setObjectName("frame_category_6")
        self.label_11 = QtWidgets.QLabel(self.frame_category_6)
        self.label_11.setGeometry(QtCore.QRect(120, 18, 124, 34))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(16)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.logo_4 = QtWidgets.QLabel(self.frame_category_6)
        self.logo_4.setGeometry(QtCore.QRect(40, 10, 61, 51))
        self.logo_4.setText("")
        self.logo_4.setPixmap(QtGui.QPixmap("UI\\../img/traduction.png"))
        self.logo_4.setScaledContents(True)
        self.logo_4.setObjectName("logo_4")
        self.scrollArea.setWidget(self.bar_nav)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1021, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.enter_email_connection.setPlaceholderText(_translate("MainWindow", "Addresse email"))
        self.label_connection_2.setText(_translate("MainWindow", "Connection"))
        self.enter_password_connection.setPlaceholderText(_translate("MainWindow", "Mot de passe"))
        self.bnt_connection.setText(_translate("MainWindow", "Se connecter"))
        self.lien_subscription.setText(_translate("MainWindow", "Inscrivez-vous ici"))
        self.label_unitile.setText(_translate("MainWindow", "Vous n\'avez pas de compte ?"))
        self.enter_email.setPlaceholderText(_translate("MainWindow", "Addresse email"))
        self.bnt_subcription.setText(_translate("MainWindow", "Inscription"))
        self.enter_last_name.setPlaceholderText(_translate("MainWindow", "Nom"))
        self.enter_first_name.setPlaceholderText(_translate("MainWindow", "Prénom"))
        self.enter_password_2.setPlaceholderText(_translate("MainWindow", "Comfirmer le mot de passe"))
        self.enter_password_1.setPlaceholderText(_translate("MainWindow", "Mot de passe"))
        self.label_subscription.setText(_translate("MainWindow", "Inscription"))
        self.lien_connection.setText(_translate("MainWindow", "Connecter vous ici"))
        self.label_unitile_2.setText(_translate("MainWindow", "Vous avez déha un compte ?"))
        self.label_connection.setText(_translate("MainWindow", "Connection"))
        self.label.setText(_translate("MainWindow", "Forums"))
        self.label_matire_scientifique.setText(_translate("MainWindow", "Matiére scientifique"))
        self.label_9.setText(_translate("MainWindow", "Philosophie"))
        self.label_4.setText(_translate("MainWindow", "Mathématique"))
        self.label_7.setText(_translate("MainWindow", "Physique"))
        self.label_8.setText(_translate("MainWindow", "SVT"))
        self.label_10.setText(_translate("MainWindow", "Français"))
        self.label_matiere_litraire.setText(_translate("MainWindow", "Matiére litéraire"))
        self.label_11.setText(_translate("MainWindow", "Anglais"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
