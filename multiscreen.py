# -*- coding: utf-8 -*-

from sqlite3 import connect
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 568)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.navbar = QtWidgets.QFrame(self.centralwidget)
        self.navbar.setGeometry(QtCore.QRect(170, 0, 401, 42))
        self.navbar.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.navbar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.navbar.setObjectName("navbar")
        self.bnt_page_1 = QtWidgets.QPushButton(self.navbar)
        self.bnt_page_1.setGeometry(QtCore.QRect(30, 4, 113, 32))
        self.bnt_page_1.setObjectName("bnt_page_1")
        self.bnt_page_2 = QtWidgets.QPushButton(self.navbar)
        self.bnt_page_2.setGeometry(QtCore.QRect(150, 4, 113, 32))
        self.bnt_page_2.setObjectName("bnt_page_2")
        self.bnt_page_3 = QtWidgets.QPushButton(self.navbar)
        self.bnt_page_3.setGeometry(QtCore.QRect(270, 5, 113, 32))
        self.bnt_page_3.setObjectName("bnt_page_3")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(160, 50, 401, 351))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.stackedWidget = QtWidgets.QStackedWidget(self.frame)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 401, 351))
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_1 = QtWidgets.QWidget()
        self.page_1.setObjectName("page_1")
        self.label_1 = QtWidgets.QLabel(self.page_1)
        self.label_1.setGeometry(QtCore.QRect(160, 120, 121, 61))
        font = QtGui.QFont()
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.label_1.setFont(font)
        self.label_1.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.label_1.setObjectName("label_1")
        self.stackedWidget.addWidget(self.page_1)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.label_2 = QtWidgets.QLabel(self.page_2)
        self.label_2.setGeometry(QtCore.QRect(150, 150, 121, 61))
        font = QtGui.QFont()
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.label_3 = QtWidgets.QLabel(self.page_3)
        self.label_3.setGeometry(QtCore.QRect(160, 160, 121, 61))
        font = QtGui.QFont()
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.stackedWidget.addWidget(self.page_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        # Pages
        # Page 1
        self.bnt_page_1.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_1))

        # Page 2
        self.bnt_page_2.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_2))
    
        # Page 3
        self.bnt_page_3.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_3))
    
     

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.bnt_page_1.setText(_translate("MainWindow", "Page 1"))
        self.bnt_page_2.setText(_translate("MainWindow", "Page 2"))
        self.bnt_page_3.setText(_translate("MainWindow", "Page 3"))
        self.label_1.setText(_translate("MainWindow", "Page 1"))
        self.label_2.setText(_translate("MainWindow", "Page 2"))
        self.label_3.setText(_translate("MainWindow", "Page 3"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
