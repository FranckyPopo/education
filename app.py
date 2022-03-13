import os
import sqlite3
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

# Nous créons le dossier qui va cotenir les bd
folder_current = os.getcwd()
folder_bd = os.path.join(folder_current, "data")
os.makedirs(folder_bd, exist_ok="yes")

class Label(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        QtWidgets.QLabel.__init__(self, parent=parent)

    def mousePressEvent(self, event):
        self.clicked.emit()
        
class Ui_MainWindow(object):
    def window_subscription(self):
        self.stacked_widget_main.setCurrentWidget(self.page_subcription)

    def window_connection(self):
        self.stacked_widget_main.setCurrentWidget(self.pag_connection)
                
    def creation_database(self, name_bd, name_table): 
        """
        Cette fonction va permetre de crée une bd

        Args:
            name_bd (str): le nom de la basse de donné
            name_table (str): le nom de la table a crée
        """
        
        conn = sqlite3.connect(folder_bd + "/" + name_bd)
        cursor = conn.cursor()
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {name_table}(
            last_name text,
            first_name text,
            email text,
            class text,
            gender text,
            password text) """)
        conn.commit()
        conn.close
    
    def get_data(self, name_bd, name_table):
        """
        Cette fonction va permetre de récupérer les infos d'une bd

        Args:
            name_bd (str): le nom de la basse de donné
            name_table (_type_): le nom de la table a crée

        Returns:
            tuple: La fonction nous retourne les données
        """
        conn = sqlite3.connect(folder_bd + "/" + name_bd)
        cursor = conn.cursor()
        data = cursor.execute(f"SELECT * FROM {name_table}").fetchall()
        conn.commit()
        conn.close()
        
        return data

    def recording_data_etudiant(self):
        self.creation_database("etudiants.bd", "etudiants")
        last_name = self.enter_last_name.text()
        first_name = self.enter_first_name.text()
        email = self.enter_email.text()
        gender = self.gender.currentText()
        clas = self.cls.currentText()
        password_1 = self.enter_password_1.text()
        password_2 = self.enter_password_2.text()
        
        if last_name and first_name and email and gender and clas and password_1 == password_2:
            d = {
                "last_name": last_name, 
                "first_name": first_name,
                "email": email,
                "gender": gender,
                "class": clas,
                "password": password_1
            }
            conn = sqlite3.connect(folder_bd + "/" + "etudiants.bd")
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO etudiants VALUES (:last_name, 
                        :first_name,
                        :email,
                        :gender,
                        :class,
                        :password)""", d)
            conn.commit()
            conn.close()
        else:
            self.alert = QtWidgets.QMessageBox()
            self.alert.about("Title", "Message")
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(993, 685)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.stacked_widget_main = QtWidgets.QStackedWidget(self.centralwidget)
        self.stacked_widget_main.setGeometry(QtCore.QRect(-10, 0, 1001, 681))
        self.stacked_widget_main.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.stacked_widget_main.setStyleSheet("")
        self.stacked_widget_main.setMidLineWidth(-2)
        self.stacked_widget_main.setObjectName("stacked_widget_main")
        self.page_index = QtWidgets.QWidget()
        self.page_index.setObjectName("page_index")
        self.frame_logo = QtWidgets.QFrame(self.page_index)
        self.frame_logo.setGeometry(QtCore.QRect(10, -1, 991, 101))
        self.frame_logo.setStyleSheet("""QFrame#frame_logo{
        background-color: rgb(255, 255, 255);
        border: 1px solid rgb(126, 126, 126);
        border-top: 0px;
        border-left: 0px;
        border-right: 0px;
        }""")
        self.frame_logo.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_logo.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_logo.setObjectName("frame_logo")
        self.bnt_connection = QtWidgets.QPushButton(self.frame_logo)
        self.bnt_connection.setGeometry(QtCore.QRect(780, 36, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.bnt_connection.setFont(font)
        self.bnt_connection.setStyleSheet("""QPushButton#bnt_connection {
        background-color: rgb(255, 255, 255);
        border: 2px solid rgb(0, 0, 255, 180);
        border-radius: 5px;
        color: rgb(0, 0, 255);
        }

        QPushButton#bnt_connection::hover {
        background-color: rgb(0, 0, 255, 180);
        color: rgb(255, 255, 255);
        } """)
        self.bnt_connection.setObjectName("bnt_connection")
        self.logo_app = QtWidgets.QLabel(self.frame_logo)
        self.logo_app.setGeometry(QtCore.QRect(41, 14, 71, 71))
        self.logo_app.setText("")
        self.logo_app.setPixmap(QtGui.QPixmap("UI/../img/bulle-de-chat.png"))
        self.logo_app.setScaledContents(True)
        self.logo_app.setObjectName("logo_app")
        self.bnt_subcription = QtWidgets.QPushButton(self.frame_logo)
        self.bnt_subcription.setGeometry(QtCore.QRect(622, 35, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.bnt_subcription.setFont(font)
        self.bnt_subcription.setStyleSheet("""QPushButton#bnt_subcription {
        background-color: rgb(255, 255, 255);
        border: 2px solid rgb(2, 163, 0);
        border-radius: 5px;
        color: rgb(2, 163, 0);
        }

        QPushButton#bnt_subcription::hover {
        background-color: rgb(2, 163, 0);
        color: rgb(255, 255, 255);
        } """)
        self.bnt_subcription.setObjectName("bnt_subcription")
        self.label_2 = QtWidgets.QLabel(self.frame_logo)
        self.label_2.setGeometry(QtCore.QRect(470, 50, 60, 16))
        self.label_2.setObjectName("label_2")
        self.frame_forums = QtWidgets.QFrame(self.page_index)
        self.frame_forums.setGeometry(QtCore.QRect(30, 101, 941, 541))
        self.frame_forums.setStyleSheet("""QFrame#frame_forums {
        background-color: rgb(255, 255, 255);
        }""")
        self.frame_forums.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_forums.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_forums.setObjectName("frame_forums")
        self.label = QtWidgets.QLabel(self.frame_forums)
        self.label.setGeometry(QtCore.QRect(40, 30, 191, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.frame_forum_math = QtWidgets.QFrame(self.frame_forums)
        self.frame_forum_math.setGeometry(QtCore.QRect(38, 130, 401, 141))
        self.frame_forum_math.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.frame_forum_math.setStyleSheet("""QFrame#frame_forum_math{
        background-color: rgb(236, 236, 236);
        border-radius: 3px;
        }

        QFrame#frame_forum_math::hover {
        background-color: rgb(204, 204, 204);
        }""")
        self.frame_forum_math.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_forum_math.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_forum_math.setObjectName("frame_forum_math")
        self.logo_math = QtWidgets.QLabel(self.frame_forum_math)
        self.logo_math.setGeometry(QtCore.QRect(14, 20, 81, 91))
        self.logo_math.setText("")
        self.logo_math.setPixmap(QtGui.QPixmap("UI/../img/math.png"))
        self.logo_math.setScaledContents(True)
        self.logo_math.setObjectName("logo_math")
        self.label_math = QtWidgets.QLabel(self.frame_forum_math)
        self.label_math.setGeometry(QtCore.QRect(116, 26, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_math.setFont(font)
        self.label_math.setObjectName("label_math")
        self.label_description_math_1 = QtWidgets.QLabel(self.frame_forum_math)
        self.label_description_math_1.setGeometry(QtCore.QRect(116, 60, 271, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_description_math_1.setFont(font)
        self.label_description_math_1.setStyleSheet("")
        self.label_description_math_1.setWordWrap(False)
        self.label_description_math_1.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard)
        self.label_description_math_1.setObjectName("label_description_math_1")
        self.label_description_math_2 = QtWidgets.QLabel(self.frame_forum_math)
        self.label_description_math_2.setGeometry(QtCore.QRect(118, 90, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_description_math_2.setFont(font)
        self.label_description_math_2.setStyleSheet("")
        self.label_description_math_2.setWordWrap(False)
        self.label_description_math_2.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard)
        self.label_description_math_2.setObjectName("label_description_math_2")
        self.label_matiere_1 = QtWidgets.QLabel(self.frame_forums)
        self.label_matiere_1.setGeometry(QtCore.QRect(40, 80, 161, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.label_matiere_1.setFont(font)
        self.label_matiere_1.setObjectName("label_matiere_1")
        self.frame_forum_physique = QtWidgets.QFrame(self.frame_forums)
        self.frame_forum_physique.setGeometry(QtCore.QRect(490, 130, 401, 141))
        self.frame_forum_physique.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.frame_forum_physique.setStyleSheet("""QFrame#frame_forum_physique{
        background-color: rgb(236, 236, 236);
        border-radius: 3px;
        }

        QFrame#frame_forum_physique::hover {
        background-color: rgb(204, 204, 204);
        }""")
        self.frame_forum_physique.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_forum_physique.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_forum_physique.setObjectName("frame_forum_physique")
        self.logo_physique = QtWidgets.QLabel(self.frame_forum_physique)
        self.logo_physique.setGeometry(QtCore.QRect(14, 20, 81, 91))
        self.logo_physique.setText("")
        self.logo_physique.setPixmap(QtGui.QPixmap("UI/../img/icons8-physique-100.png"))
        self.logo_physique.setScaledContents(True)
        self.logo_physique.setObjectName("logo_physique")
        self.label_physique = QtWidgets.QLabel(self.frame_forum_physique)
        self.label_physique.setGeometry(QtCore.QRect(116, 26, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_physique.setFont(font)
        self.label_physique.setObjectName("label_physique")
        self.label_description_physique_1 = QtWidgets.QLabel(self.frame_forum_physique)
        self.label_description_physique_1.setGeometry(QtCore.QRect(116, 60, 271, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_description_physique_1.setFont(font)
        self.label_description_physique_1.setStyleSheet("")
        self.label_description_physique_1.setWordWrap(False)
        self.label_description_physique_1.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard)
        self.label_description_physique_1.setObjectName("label_description_physique_1")
        self.label_description_physique_2 = QtWidgets.QLabel(self.frame_forum_physique)
        self.label_description_physique_2.setGeometry(QtCore.QRect(118, 90, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_description_physique_2.setFont(font)
        self.label_description_physique_2.setStyleSheet("")
        self.label_description_physique_2.setWordWrap(False)
        self.label_description_physique_2.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard)
        self.label_description_physique_2.setObjectName("label_description_physique_2")
        self.label_matiere_2 = QtWidgets.QLabel(self.frame_forums)
        self.label_matiere_2.setGeometry(QtCore.QRect(40, 320, 161, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.label_matiere_2.setFont(font)
        self.label_matiere_2.setObjectName("label_matiere_2")
        self.frame_forum_philo = QtWidgets.QFrame(self.frame_forums)
        self.frame_forum_philo.setGeometry(QtCore.QRect(492, 360, 401, 141))
        self.frame_forum_philo.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.frame_forum_philo.setStyleSheet("""QFrame#frame_forum_philo{
        background-color: rgb(236, 236, 236);
        border-radius: 3px;
        }

        QFrame#frame_forum_philo::hover {
        background-color: rgb(204, 204, 204);
        }""")
        self.frame_forum_philo.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_forum_philo.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_forum_philo.setObjectName("frame_forum_philo")
        self.logo_physique_3 = QtWidgets.QLabel(self.frame_forum_philo)
        self.logo_physique_3.setGeometry(QtCore.QRect(14, 20, 81, 91))
        self.logo_physique_3.setText("")
        self.logo_physique_3.setPixmap(QtGui.QPixmap("UI/../../img/math.png"))
        self.logo_physique_3.setScaledContents(True)
        self.logo_physique_3.setObjectName("logo_physique_3")
        self.label_physique_3 = QtWidgets.QLabel(self.frame_forum_philo)
        self.label_physique_3.setGeometry(QtCore.QRect(116, 26, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_physique_3.setFont(font)
        self.label_physique_3.setObjectName("label_physique_3")
        self.label_description_physique_5 = QtWidgets.QLabel(self.frame_forum_philo)
        self.label_description_physique_5.setGeometry(QtCore.QRect(116, 60, 271, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_description_physique_5.setFont(font)
        self.label_description_physique_5.setStyleSheet("")
        self.label_description_physique_5.setWordWrap(False)
        self.label_description_physique_5.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard)
        self.label_description_physique_5.setObjectName("label_description_physique_5")
        self.label_description_physique_6 = QtWidgets.QLabel(self.frame_forum_philo)
        self.label_description_physique_6.setGeometry(QtCore.QRect(118, 90, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_description_physique_6.setFont(font)
        self.label_description_physique_6.setStyleSheet("")
        self.label_description_physique_6.setWordWrap(False)
        self.label_description_physique_6.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard)
        self.label_description_physique_6.setObjectName("label_description_physique_6")
        self.frame_forum_francais = QtWidgets.QFrame(self.frame_forums)
        self.frame_forum_francais.setGeometry(QtCore.QRect(40, 370, 401, 141))
        self.frame_forum_francais.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.frame_forum_francais.setStyleSheet("""QFrame#frame_forum_francais{
        background-color: rgb(236, 236, 236);
        border-radius: 3px;
        }

        QFrame#frame_forum_francais::hover {
        background-color: rgb(204, 204, 204);
        }""")
        self.frame_forum_francais.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_forum_francais.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_forum_francais.setObjectName("frame_forum_francais")
        self.logo_francais = QtWidgets.QLabel(self.frame_forum_francais)
        self.logo_francais.setGeometry(QtCore.QRect(14, 20, 81, 91))
        self.logo_francais.setText("")
        self.logo_francais.setPixmap(QtGui.QPixmap("UI/../../img/math.png"))
        self.logo_francais.setScaledContents(True)
        self.logo_francais.setObjectName("logo_francais")
        self.label_francais = QtWidgets.QLabel(self.frame_forum_francais)
        self.label_francais.setGeometry(QtCore.QRect(116, 26, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_francais.setFont(font)
        self.label_francais.setObjectName("label_francais")
        self.label_description_francais = QtWidgets.QLabel(self.frame_forum_francais)
        self.label_description_francais.setGeometry(QtCore.QRect(116, 60, 271, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_description_francais.setFont(font)
        self.label_description_francais.setStyleSheet("")
        self.label_description_francais.setWordWrap(False)
        self.label_description_francais.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard)
        self.label_description_francais.setObjectName("label_description_francais")
        self.label_description_francais_2 = QtWidgets.QLabel(self.frame_forum_francais)
        self.label_description_francais_2.setGeometry(QtCore.QRect(118, 90, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_description_francais_2.setFont(font)
        self.label_description_francais_2.setStyleSheet("")
        self.label_description_francais_2.setWordWrap(False)
        self.label_description_francais_2.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard)
        self.label_description_francais_2.setObjectName("label_description_francais_2")
        self.stacked_widget_main.addWidget(self.page_index)
        self.pageadmin = QtWidgets.QWidget()
        self.pageadmin.setObjectName("pageadmin")
        self.frame_logo_6 = QtWidgets.QFrame(self.pageadmin)
        self.frame_logo_6.setGeometry(QtCore.QRect(10, 0, 991, 121))
        self.frame_logo_6.setStyleSheet("""QFrame#frame_logo_6{
        background-color: rgb(255, 255, 255);
        border: 1px solid rgb(126, 126, 126);
        border-top: 0px;
        border-left: 0px;
        border-right: 0px;
        }""")
        self.frame_logo_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_logo_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_logo_6.setObjectName("frame_logo_6")
        self.logo_app_6 = QtWidgets.QLabel(self.frame_logo_6)
        self.logo_app_6.setGeometry(QtCore.QRect(46, 22, 71, 71))
        self.logo_app_6.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.logo_app_6.setText("")
        self.logo_app_6.setPixmap(QtGui.QPixmap("UI/../img/bulle-de-chat.png"))
        self.logo_app_6.setScaledContents(True)
        self.logo_app_6.setObjectName("logo_app_6")
        self.frame_controler = QtWidgets.QFrame(self.frame_logo_6)
        self.frame_controler.setGeometry(QtCore.QRect(749, 2, 181, 111))
        self.frame_controler.setStyleSheet("QFrame#frame_controler{\n"
"border: 0px solid;\n"
"}")
        self.frame_controler.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_controler.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_controler.setObjectName("frame_controler")
        self.bnt_space_etudiant = QtWidgets.QPushButton(self.frame_controler)
        self.bnt_space_etudiant.setGeometry(QtCore.QRect(1, 10, 171, 41))
        self.bnt_space_etudiant.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bnt_space_etudiant.setStyleSheet("QPushButton#bnt_space_etudiant {\n"
"background-color: rgb(77, 86, 255);\n"
"border-radius: 20px;\n"
"color: white;\n"
"}\n"
"\n"
"QPushButton#bnt_space_etudiant::hover {\n"
"background-color: rgb(90, 79, 255);\n"
"}\n"
"")
        self.bnt_space_etudiant.setObjectName("bnt_space_etudiant")
        self.bnt_space_admin = QtWidgets.QPushButton(self.frame_controler)
        self.bnt_space_admin.setGeometry(QtCore.QRect(0, 60, 171, 41))
        self.bnt_space_admin.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bnt_space_admin.setStyleSheet("QPushButton#bnt_space_admin {\n"
"background-color: rgb(2, 163, 0);\n"
"border-radius: 20px;\n"
"color: white;\n"
"}\n"
"\n"
"QPushButton#bnt_space_admin::hover {\n"
"}\n"
"")
        self.bnt_space_admin.setObjectName("bnt_space_admin")
        self.frame = QtWidgets.QFrame(self.pageadmin)
        self.frame.setGeometry(QtCore.QRect(10, 160, 1001, 141))
        self.frame.setStyleSheet("QFrame#frame{ \n"
"background-color: rgb(226, 226, 226);\n"
"}\n"
"")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.bnt_list_etudiant = QtWidgets.QPushButton(self.frame)
        self.bnt_list_etudiant.setGeometry(QtCore.QRect(271, 30, 201, 81))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.bnt_list_etudiant.setFont(font)
        self.bnt_list_etudiant.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bnt_list_etudiant.setStyleSheet("QPushButton#bnt_list_etudiant {\n"
"color: white;\n"
"background-color: #4dd14b;\n"
"}")
        self.bnt_list_etudiant.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("UI/../img/groupe-de-discussion copie.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bnt_list_etudiant.setIcon(icon)
        self.bnt_list_etudiant.setIconSize(QtCore.QSize(76, 60))
        self.bnt_list_etudiant.setObjectName("bnt_list_etudiant")
        self.label_etudiant = QtWidgets.QLabel(self.frame)
        self.label_etudiant.setGeometry(QtCore.QRect(301, 112, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.label_etudiant.setFont(font)
        self.label_etudiant.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.label_etudiant.setObjectName("label_etudiant")
        self.bnt_list_discussions = QtWidgets.QPushButton(self.frame)
        self.bnt_list_discussions.setGeometry(QtCore.QRect(499, 30, 201, 81))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.bnt_list_discussions.setFont(font)
        self.bnt_list_discussions.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bnt_list_discussions.setStyleSheet("QPushButton#bnt_list_discussions {\n"
"color: white;\n"
"background-color: #4dd14b;\n"
"\n"
"}")
        self.bnt_list_discussions.setText("")
        self.bnt_list_discussions.setIcon(icon)
        self.bnt_list_discussions.setIconSize(QtCore.QSize(76, 60))
        self.bnt_list_discussions.setObjectName("bnt_list_discussions")
        self.label_discussions = QtWidgets.QLabel(self.frame)
        self.label_discussions.setGeometry(QtCore.QRect(531, 110, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.label_discussions.setFont(font)
        self.label_discussions.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.label_discussions.setObjectName("label_discussions")
        self.stacked_widget_list_infos = QtWidgets.QStackedWidget(self.pageadmin)
        self.stacked_widget_list_infos.setGeometry(QtCore.QRect(0, 300, 1001, 371))
        self.stacked_widget_list_infos.setStyleSheet("QStackedWidget#stacked_widget_list_infos{\n"
"background-color: rgb(255, 255, 255);\n"
"}")
        self.stacked_widget_list_infos.setObjectName("stacked_widget_list_infos")
        self.page_liste_etudiant = QtWidgets.QWidget()
        self.page_liste_etudiant.setObjectName("page_liste_etudiant")
        self.label_etudiant_2 = QtWidgets.QLabel(self.page_liste_etudiant)
        self.label_etudiant_2.setGeometry(QtCore.QRect(80, 20, 151, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label_etudiant_2.setFont(font)
        self.label_etudiant_2.setObjectName("label_etudiant_2")
        self.frame_list_etudiant = QtWidgets.QFrame(self.page_liste_etudiant)
        self.frame_list_etudiant.setGeometry(QtCore.QRect(80, 60, 891, 101))
        self.frame_list_etudiant.setStyleSheet("QFrame#frame_list_etudiant {\n"
"background-color: rgb(226, 226, 226);\n"
"border-radius: 5px;\n"
"}")
        self.frame_list_etudiant.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_list_etudiant.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_list_etudiant.setObjectName("frame_list_etudiant")
        self.stacked_widget_list_infos.addWidget(self.page_liste_etudiant)
        self.page_list_discussions = QtWidgets.QWidget()
        self.page_list_discussions.setObjectName("page_list_discussions")
        self.frame_list_discussions = QtWidgets.QFrame(self.page_list_discussions)
        self.frame_list_discussions.setGeometry(QtCore.QRect(80, 70, 891, 101))
        self.frame_list_discussions.setStyleSheet("QFrame#frame_list_etudiant {\n"
"background-color: rgb(226, 226, 226);\n"
"border-radius: 5px;\n"
"}")
        self.frame_list_discussions.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_list_discussions.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_list_discussions.setObjectName("frame_list_discussions")
        self.label_disscussions = QtWidgets.QLabel(self.page_list_discussions)
        self.label_disscussions.setGeometry(QtCore.QRect(80, 30, 151, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label_disscussions.setFont(font)
        self.label_disscussions.setObjectName("label_disscussions")
        self.stacked_widget_list_infos.addWidget(self.page_list_discussions)
        self.stacked_widget_main.addWidget(self.pageadmin)
        self.page_subcription = QtWidgets.QWidget()
        self.page_subcription.setObjectName("page_subcription")
        self.frame_logo_2 = QtWidgets.QFrame(self.page_subcription)
        self.frame_logo_2.setGeometry(QtCore.QRect(10, 0, 981, 101))
        self.frame_logo_2.setStyleSheet("QFrame#frame_logo_2{\n"
"background-color: rgb(255, 255, 255);\n"
"border: 1px solid rgb(126, 126, 126);\n"
"border-top: 0px;\n"
"border-left: 0px;\n"
"border-right: 0px;\n"
"}")
        self.frame_logo_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_logo_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_logo_2.setObjectName("frame_logo_2")
        self.logo_app_2 = QtWidgets.QLabel(self.frame_logo_2)
        self.logo_app_2.setGeometry(QtCore.QRect(41, 14, 71, 71))
        self.logo_app_2.setText("")
        self.logo_app_2.setPixmap(QtGui.QPixmap("UI/../img/bulle-de-chat.png"))
        self.logo_app_2.setScaledContents(True)
        self.logo_app_2.setObjectName("logo_app_2")
        self.frame_subcription_left = QtWidgets.QFrame(self.page_subcription)
        self.frame_subcription_left.setGeometry(QtCore.QRect(10, 101, 461, 561))
        self.frame_subcription_left.setMaximumSize(QtCore.QSize(468, 16777215))
        font = QtGui.QFont()
        font.setPointSize(5)
        self.frame_subcription_left.setFont(font)
        self.frame_subcription_left.setFocusPolicy(QtCore.Qt.NoFocus)
        self.frame_subcription_left.setToolTip("")
        self.frame_subcription_left.setStyleSheet("QFrame#frame_subcription_left{\n"
"background-color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"")
        self.frame_subcription_left.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_subcription_left.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_subcription_left.setObjectName("frame_subcription_left")
        self.label_subcription = QtWidgets.QLabel(self.frame_subcription_left)
        self.label_subcription.setGeometry(QtCore.QRect(180, 17, 121, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label_subcription.setFont(font)
        self.label_subcription.setObjectName("label_subcription")
        self.enter_last_name = QtWidgets.QLineEdit(self.frame_subcription_left)
        self.enter_last_name.setGeometry(QtCore.QRect(100, 70, 291, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.enter_last_name.setFont(font)
        self.enter_last_name.setStyleSheet("QLineEdit#enter_last_name{\n"
"padding: 10px;\n"
"border-top: 1px solid rgb(236, 236, 236);\n"
"border-left: 1px solid rgb(236, 236, 236);\n"
"border-right: 1px solid rgb(236, 236, 236);\n"
"border-bottom: 1px solid black;\n"
"border-radius: 5px;\n"
"}\n"
"\n"
"QLineEdit#enter_last_name::hover {\n"
"border-bottom: 2px solid rgb(0, 0, 255);\n"
"}\n"
"\n"
"")
        self.enter_last_name.setObjectName("enter_last_name")
        self.enter_first_name = QtWidgets.QLineEdit(self.frame_subcription_left)
        self.enter_first_name.setGeometry(QtCore.QRect(100, 130, 291, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.enter_first_name.setFont(font)
        self.enter_first_name.setStyleSheet("QLineEdit#enter_first_name{\n"
"padding: 10px;\n"
"border-top: 1px solid rgb(236, 236, 236);\n"
"border-left: 1px solid rgb(236, 236, 236);\n"
"border-right: 1px solid rgb(236, 236, 236);\n"
"border-bottom: 1px solid black;\n"
"border-radius: 5px;\n"
"}\n"
"\n"
"QLineEdit#enter_first_name::hover {\n"
"border-bottom: 2px solid rgb(0, 0, 255);\n"
"}\n"
"\n"
"")
        self.enter_first_name.setObjectName("enter_first_name")
        self.enter_email = QtWidgets.QLineEdit(self.frame_subcription_left)
        self.enter_email.setGeometry(QtCore.QRect(100, 190, 291, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.enter_email.setFont(font)
        self.enter_email.setStyleSheet("QLineEdit#enter_email{\n"
"padding: 10px;\n"
"border-top: 1px solid rgb(236, 236, 236);\n"
"border-left: 1px solid rgb(236, 236, 236);\n"
"border-right: 1px solid rgb(236, 236, 236);\n"
"border-bottom: 1px solid black;\n"
"border-radius: 5px;\n"
"}\n"
"\n"
"QLineEdit#enter_email::hover {\n"
"border-bottom: 2px solid rgb(0, 0, 255);\n"
"}\n"
"\n"
"")
        self.enter_email.setText("")
        self.enter_email.setCursorMoveStyle(QtCore.Qt.VisualMoveStyle)
        self.enter_email.setObjectName("enter_email")
        self.enter_password_1 = QtWidgets.QLineEdit(self.frame_subcription_left)
        self.enter_password_1.setGeometry(QtCore.QRect(100, 343, 291, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.enter_password_1.setFont(font)
        self.enter_password_1.setStyleSheet("QLineEdit#enter_password_1{\n"
"padding: 10px;\n"
"border-top: 1px solid rgb(236, 236, 236);\n"
"border-left: 1px solid rgb(236, 236, 236);\n"
"border-right: 1px solid rgb(236, 236, 236);\n"
"border-bottom: 1px solid black;\n"
"border-radius: 5px;\n"
"}\n"
"\n"
"QLineEdit#enter_password_1::hover {\n"
"border-bottom: 2px solid rgb(0, 0, 255);\n"
"}\n"
"\n"
"")
        self.enter_password_1.setText("")
        self.enter_password_1.setCursorMoveStyle(QtCore.Qt.VisualMoveStyle)
        self.enter_password_1.setObjectName("enter_password_1")
        self.enter_password_2 = QtWidgets.QLineEdit(self.frame_subcription_left)
        self.enter_password_2.setGeometry(QtCore.QRect(100, 400, 291, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.enter_password_2.setFont(font)
        self.enter_password_2.setStyleSheet("QLineEdit#enter_password_2{\n"
"padding: 10px;\n"
"border-top: 1px solid rgb(236, 236, 236);\n"
"border-left: 1px solid rgb(236, 236, 236);\n"
"border-right: 1px solid rgb(236, 236, 236);\n"
"border-bottom: 1px solid black;\n"
"border-radius: 5px;\n"
"}\n"
"\n"
"QLineEdit#enter_password_2::hover {\n"
"border-bottom: 2px solid rgb(0, 0, 255);\n"
"}\n"
"\n"
"")
        self.enter_password_2.setText("")
        self.enter_password_2.setCursorMoveStyle(QtCore.Qt.VisualMoveStyle)
        self.enter_password_2.setObjectName("enter_password_2")
        self.gender = QtWidgets.QComboBox(self.frame_subcription_left)
        self.gender.addItem("Homme")
        self.gender.addItem("Femme")
        self.gender.setGeometry(QtCore.QRect(100, 250, 291, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.gender.setFont(font)
        self.gender.setStyleSheet("QComboBox#gender {"
        "background-color: rgb(255, 255, 255);"
        "color: black;"
        "border-top: 1px solid rgb(236, 236, 236);"
        "border-left: 1px solid rgb(236, 236, 236);"
        "border-right: 1px solid rgb(236, 236, 236);"
        "border-bottom: 1px solid black;"
        "}"

        "QComboBox#gender;;hover {"
        "border-bottom: 1px solid rgb(0, 0, 255);"
        "color: black;"
        "}")
        self.gender.setEditable(False)
        self.gender.setMaxVisibleItems(13)
        self.gender.setDuplicatesEnabled(False)
        self.gender.setObjectName("gender")
        self.cls = QtWidgets.QComboBox(self.frame_subcription_left)
        self.cls.setGeometry(QtCore.QRect(100, 300, 291, 31))
        list_class = ["6éme", "5éme", "4éme", "3éme", "2nd", "1ère", "Terminal", "autres"]
        for item in list_class: self.cls.addItem(item)
        self.cls.setFont(font)
        self.cls.setObjectName("cls")
        self.cls.setStyleSheet("QComboBox#cls {"
        "background-color: rgb(255, 255, 255);"
        "color: black;"
        "border-top: 1px solid rgb(236, 236, 236);"
        "border-left: 1px solid rgb(236, 236, 236);"
        "border-right: 1px solid rgb(236, 236, 236);"
        "border-bottom: 1px solid black;"
        "}"

        "QComboBox#cls;;hover {"
        "border-bottom: 1px solid rgb(0, 0, 255);"
        "color: black;"
        "}")
        self.cls.setEditable(False)
        
        self.bnt_subcription_2 = QtWidgets.QPushButton(self.frame_subcription_left)
        self.bnt_subcription_2.setGeometry(QtCore.QRect(100, 455, 291, 41))
        self.bnt_subcription_2.clicked.connect(self.recording_data_etudiant)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.bnt_subcription_2.setFont(font)
        self.bnt_subcription_2.setStyleSheet("QPushButton#bnt_subcription_2 {\n"
"background-color: rgb(255, 255, 255);\n"
"border: 2px solid rgb(0, 0, 255, 180);\n"
"border-radius: 5px;\n"
"color: rgb(0, 0, 255);\n"
"}\n"
"\n"
"QPushButton#bnt_subcription_2::hover {\n"
"background-color: rgba(0, 0, 255, 180);\n"
"color: rgb(255, 255, 255);\n"
"} ")
        self.bnt_subcription_2.setObjectName("bnt_subcription_2")
        self.label_useless_2 = QtWidgets.QLabel(self.frame_subcription_left)
        self.label_useless_2.setGeometry(QtCore.QRect(100, 502, 181, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.label_useless_2.setFont(font)
        self.label_useless_2.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.label_useless_2.setObjectName("label_useless_2")
        self.label_connection_account = Label(self.frame_subcription_left)
        self.label_connection_account.setGeometry(QtCore.QRect(285, 502, 111, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.label_connection_account.setFont(font)
        self.label_connection_account.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.label_connection_account.setStyleSheet("QLabel#label_connection_account {\n"
"color: rgb(0, 0, 255);\n"
"}")
        self.label_connection_account.setObjectName("label_connection_account")
        self.frame_subcription_right = QtWidgets.QFrame(self.page_subcription)
        self.frame_subcription_right.setGeometry(QtCore.QRect(472, 102, 521, 561))
        self.frame_subcription_right.setStyleSheet("QFrame#frame_subcription_right{\n"
"background-color:rgba(0, 0, 255, 180);\n"
"}\n"
"\n"
"")
        self.frame_subcription_right.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_subcription_right.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_subcription_right.setObjectName("frame_subcription_right")
        self.label_motivation = QtWidgets.QLabel(self.frame_subcription_right)
        self.label_motivation.setGeometry(QtCore.QRect(190, 240, 181, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_motivation.setFont(font)
        self.label_motivation.setStyleSheet("QLabel#label_motivation {\n"
"color: rgb(255, 255, 255);\n"
"}")
        self.label_motivation.setObjectName("label_motivation")
        self.stacked_widget_main.addWidget(self.page_subcription)
        self.pag_connection = QtWidgets.QWidget()
        self.pag_connection.setObjectName("pag_connection")
        self.frame_connection_left = QtWidgets.QFrame(self.pag_connection)
        self.frame_connection_left.setGeometry(QtCore.QRect(8, 100, 461, 561))
        self.frame_connection_left.setMaximumSize(QtCore.QSize(468, 16777215))
        font = QtGui.QFont()
        font.setPointSize(5)
        self.frame_connection_left.setFont(font)
        self.frame_connection_left.setFocusPolicy(QtCore.Qt.NoFocus)
        self.frame_connection_left.setToolTip("")
        self.frame_connection_left.setStyleSheet("QFrame#frame_connection_left{\n"
"background-color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"")
        self.frame_connection_left.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_connection_left.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_connection_left.setObjectName("frame_connection_left")
        self.label_connection = QtWidgets.QLabel(self.frame_connection_left)
        self.label_connection.setGeometry(QtCore.QRect(150, 120, 131, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label_connection.setFont(font)
        self.label_connection.setObjectName("label_connection")
        self.enter_email_connection = QtWidgets.QLineEdit(self.frame_connection_left)
        self.enter_email_connection.setGeometry(QtCore.QRect(50, 190, 341, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.enter_email_connection.setFont(font)
        self.enter_email_connection.setStyleSheet("QLineEdit#enter_email_connection{\n"
"padding: 10px;\n"
"border-top: 1px solid rgb(236, 236, 236);\n"
"border-left: 1px solid rgb(236, 236, 236);\n"
"border-right: 1px solid rgb(236, 236, 236);\n"
"border-bottom: 1px solid black;\n"
"border-radius: 5px;\n"
"}\n"
"\n"
"QLineEdit#enter_email_connection::hover {\n"
"border-bottom: 2px solid rgb(0, 0, 255);\n"
"}\n"
"\n"
"")
        self.enter_email_connection.setObjectName("enter_email_connection")
        self.enter_password_connection = QtWidgets.QLineEdit(self.frame_connection_left)
        self.enter_password_connection.setGeometry(QtCore.QRect(50, 250, 341, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.enter_password_connection.setFont(font)
        self.enter_password_connection.setStyleSheet("QLineEdit#enter_password_connection{\n"
"padding: 10px;\n"
"border-top: 1px solid rgb(236, 236, 236);\n"
"border-left: 1px solid rgb(236, 236, 236);\n"
"border-right: 1px solid rgb(236, 236, 236);\n"
"border-bottom: 1px solid black;\n"
"border-radius: 5px;\n"
"}\n"
"\n"
"QLineEdit#enter_password_connection::hover {\n"
"border-bottom: 2px solid rgb(0, 0, 255);\n"
"}\n"
"\n"
"")
        self.enter_password_connection.setObjectName("enter_password_connection")
        self.bnt_connection_2 = QtWidgets.QPushButton(self.frame_connection_left)
        self.bnt_connection_2.setGeometry(QtCore.QRect(50, 330, 341, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.bnt_connection_2.setFont(font)
        self.bnt_connection_2.setStyleSheet("QPushButton#bnt_connection_2 {\n"
"background-color: rgb(255, 255, 255);\n"
"border: 2px solid rgb(0, 0, 255, 180);\n"
"border-radius: 5px;\n"
"color: rgb(0, 0, 255);\n"
"}\n"
"\n"
"QPushButton#bnt_connection_2::hover {\n"
"background-color: rgba(0, 0, 255, 180);\n"
"color: rgb(255, 255, 255);\n"
"} ")
        self.bnt_connection_2.setObjectName("bnt_connection_2")
        self.label_useless = QtWidgets.QLabel(self.frame_connection_left)
        self.label_useless.setGeometry(QtCore.QRect(23, 390, 241, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.label_useless.setFont(font)
        self.label_useless.setObjectName("label_useless")
        self.label_creation_account = Label(self.frame_connection_left)
        self.label_creation_account.setGeometry(QtCore.QRect(257, 390, 171, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.label_creation_account.setFont(font)
        self.label_creation_account.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.label_creation_account.setStyleSheet("QLabel#label_creation_account {\n"
"color: rgb(0, 0, 255);\n"
"}\n"
"")
        self.label_creation_account.setObjectName("label_creation_account")
        self.frame_logo_3 = QtWidgets.QFrame(self.pag_connection)
        self.frame_logo_3.setGeometry(QtCore.QRect(8, 0, 991, 101))
        self.frame_logo_3.setStyleSheet("QFrame#frame_logo_3{\n"
"background-color: rgb(255, 255, 255);\n"
"border: 1px solid rgb(126, 126, 126);\n"
"border-top: 0px;\n"
"border-left: 0px;\n"
"border-right: 0px;\n"
"}")
        self.frame_logo_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_logo_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_logo_3.setObjectName("frame_logo_3")
        self.logo_app_3 = QtWidgets.QLabel(self.frame_logo_3)
        self.logo_app_3.setGeometry(QtCore.QRect(41, 14, 71, 71))
        self.logo_app_3.setText("")
        self.logo_app_3.setPixmap(QtGui.QPixmap("UI/../img/bulle-de-chat.png"))
        self.logo_app_3.setScaledContents(True)
        self.logo_app_3.setObjectName("logo_app_3")
        self.frame_connection_right = QtWidgets.QFrame(self.pag_connection)
        self.frame_connection_right.setGeometry(QtCore.QRect(470, 101, 531, 561))
        self.frame_connection_right.setStyleSheet("QFrame#frame_connection_right{\n"
"background-color:rgba(0, 0, 255, 180);\n"
"}\n"
"\n"
"")
        self.frame_connection_right.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_connection_right.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_connection_right.setObjectName("frame_connection_right")
        self.label_motivation_2 = QtWidgets.QLabel(self.frame_connection_right)
        self.label_motivation_2.setGeometry(QtCore.QRect(190, 240, 181, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_motivation_2.setFont(font)
        self.label_motivation_2.setStyleSheet("QLabel#label_motivation_2 {\n"
"color: rgb(255, 255, 255);\n"
"}")
        self.label_motivation_2.setObjectName("label_motivation_2")
        self.stacked_widget_main.addWidget(self.pag_connection)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 993, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.stacked_widget_main.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        # Connection des fênetre entre elle
        self.bnt_connection.clicked.connect(self.window_connection)
        self.label_connection_account.clicked.connect(self.window_connection)
        self.bnt_subcription.clicked.connect(self.window_subscription)
        self.label_creation_account.clicked.connect(self.window_subscription)
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.bnt_connection.setText(_translate("MainWindow", "Se connecter"))
        self.bnt_subcription.setText(_translate("MainWindow", "S\'inscrir"))
        self.label_2.setText(_translate("MainWindow", "TextLabel"))
        self.label.setText(_translate("MainWindow", "Liste des forums"))
        self.label_math.setText(_translate("MainWindow", "Mathématique"))
        self.label_description_math_1.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">Un question en math posez la !</span></p></body></html>"))
        self.label_description_math_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">Et vous aurez une réponse</span></p></body></html>"))
        self.label_matiere_1.setText(_translate("MainWindow", "Matiére scientfique"))
        self.label_physique.setText(_translate("MainWindow", "Physique"))
        self.label_description_physique_1.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">Un question en math posez la !</span></p></body></html>"))
        self.label_description_physique_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">Et vous aurez une réponse</span></p></body></html>"))
        self.label_matiere_2.setText(_translate("MainWindow", "Matiére litéraire"))
        self.label_physique_3.setText(_translate("MainWindow", "Philosophie"))
        self.label_description_physique_5.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">Un question en math posez la !</span></p></body></html>"))
        self.label_description_physique_6.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">Et vous aurez une réponse</span></p></body></html>"))
        self.label_francais.setText(_translate("MainWindow", "Français"))
        self.label_description_francais.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">Un question en math posez la !</span></p></body></html>"))
        self.label_description_francais_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">Et vous aurez une réponse</span></p></body></html>"))
        self.bnt_space_etudiant.setText(_translate("MainWindow", "Espace etudiant"))
        self.bnt_space_admin.setText(_translate("MainWindow", "Espace administrateur"))
        self.label_etudiant.setText(_translate("MainWindow", "liste des etudiants"))
        self.label_discussions.setText(_translate("MainWindow", "liste des discussions"))
        self.label_etudiant_2.setText(_translate("MainWindow", "Liste étudians"))
        self.label_disscussions.setText(_translate("MainWindow", "Liste étudians"))
        self.label_subcription.setText(_translate("MainWindow", "Inscription"))
        self.enter_last_name.setPlaceholderText(_translate("MainWindow", "Nom"))
        self.enter_first_name.setPlaceholderText(_translate("MainWindow", "Prénom"))
        self.enter_email.setPlaceholderText(_translate("MainWindow", "Email"))
        self.enter_password_1.setPlaceholderText(_translate("MainWindow", "Mot de passe"))
        self.enter_password_2.setPlaceholderText(_translate("MainWindow", "Confirmer mot de passe"))
        self.bnt_subcription_2.setText(_translate("MainWindow", "S\'inscrir"))
        self.label_useless_2.setText(_translate("MainWindow", "Vous avez déjà un compte ?"))
        self.label_connection_account.setText(_translate("MainWindow", "Connectez-vous"))
        self.label_motivation.setText(_translate("MainWindow", "Texte a jouter"))
        self.label_connection.setText(_translate("MainWindow", "Connection"))
        self.enter_email_connection.setPlaceholderText(_translate("MainWindow", "Email"))
        self.enter_password_connection.setPlaceholderText(_translate("MainWindow", "Mot de passe"))
        self.bnt_connection_2.setText(_translate("MainWindow", "Connection"))
        self.label_useless.setText(_translate("MainWindow", "<html><head/><body><p>Vous n\'avez pas encore de compte ?</p></body></html>"))
        self.label_creation_account.setText(_translate("MainWindow", "Inscrivez-vous gratuitement"))
        self.label_motivation_2.setText(_translate("MainWindow", "Texte a jouter"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
