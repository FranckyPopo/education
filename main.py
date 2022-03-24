# -*- coding: utf-8 -*-
import os
import sqlite3
import sys
import smtplib
import string
from random import choice
from functools import partial
from datetime import datetime, date
from pprint import pprint
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

# Nous créons le dossier qui va cotenir les bd
folder_current = os.getcwd()
folder_bd = os.path.join(folder_current, "data")
folder_img = os.path.join(folder_current, "img")
os.makedirs(folder_bd, exist_ok="yes")

class Frame(QtWidgets.QFrame):
    clicked = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        QtWidgets.QFrame.__init__(self, parent=parent)

    def mousePressEvent(self, event):
        self.clicked.emit()


class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
    def window_connection(self):
        self.stackedWidget.setCurrentWidget(self.page_connection)
        
    def window_subscription(self):
        self.stackedWidget.setCurrentWidget(self.page_subscription)
        
    def window_subjets(self, name_subjet: str):
        self.stackedWidget.setCurrentWidget(self.page_subjet)
        self.display_subjet(name_subjet)
        
    def window_creat_subjet(self):
        self.stackedWidget.setCurrentWidget(self.page_creat_discuss)
        
    def window_discuss(self, id_subjet: str):
        self.stackedWidget.setCurrentWidget(self.page_discuss)
        self.display_dicuss(id_subjet)
        
    def display_subjet(self, name_subjet: str):  
        # Le programme filtre les sujets
        conn = sqlite3.connect(folder_bd + "/" + "forums.bd")
        cursor = conn.cursor()
        subjets = cursor.execute(f"SELECT * FROM subjets_forums WHERE subjet='{name_subjet}'").fetchall()
        conn.commit()
        conn.close()
        
        widget_children = self.subjet.children()
        for item in widget_children[1::]: item.deleteLater() 
            
        for i in range(self.vbox.count()): self.vbox.removeItem(self.vbox.itemAt(i))

        for subjet in reversed(subjets):
            # Récupération de l'id du sujet 
            id_subjet = subjet[6]

            frame_subjet = Frame()
            frame_subjet.clicked.connect(partial(self.window_discuss, id_subjet))
            frame_subjet.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            frame_subjet.setObjectName("frame_subjet")
            frame_subjet.setFixedSize(650, 110)
            frame_subjet.setStyleSheet("""
                QFrame#frame_subjet{
                    background-color: #cccccc;
                    border-radius: 5px;
                    margin-left: 25px;
                    margin-top: 15px;
                }
                
                QFrame#frame_subjet::hover{
                    background-color: #ececec;
                }
                
                QLabel#label_title{
                    margin-top: 30px;
                    margin-left: 50px;
                }
                
                QLabel#label_author{
                    margin-left: 50px;
                    margin-top: 70px;
                }
            """)
            title = subjet[1]
            label_title = QtWidgets.QLabel(title, frame_subjet)
            label_title.setObjectName("label_title")
            font_title = QtGui.QFont()
            font_title.setFamily("Arial")
            font_title.setPointSize(16)
            font_title.setWeight(50)
            font_title.setBold(True)
            label_title.setFont(font_title)

            # Nous récupérons les différentes information du sujet 
            date_recording_subjet = subjet[4].replace("/", "-")
            dates = date.fromisoformat(date_recording_subjet)
            author = "Afri Kreto"
            day = dates.strftime("%d %B %Y").replace("March", "mars")
            time = subjet[5]
            infos = f"Par {author} {day} {time} "
            
            label_author = QtWidgets.QLabel(frame_subjet)
            label_author.setObjectName("label_author")
            label_author.setText(infos)
            font_autor = QtGui.QFont()
            font_autor.setFamily("Arial")
            font_autor.setPointSize(14)
            font_autor.setWeight(50)
            label_author.setFont(font_autor)

            self.vbox.addWidget(frame_subjet)

        self.subjet.setLayout(self.vbox)
        
        #Scroll Area Properties
        self.contenai_subjet.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.contenai_subjet.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.contenai_subjet.setWidgetResizable(True)
        self.contenai_subjet.setWidget(self.subjet)

        
    def display_dicuss(self, id_subjet: str):
        # On supprimer les widgets
        widget_children = self.discuss.children()
        for item in widget_children[1::]: item.deleteLater() 
        for i in range(self.vbox_2.count()):self.vbox_2.removeItem(self.vbox_2.itemAt(i))
            
        conn = sqlite3.connect(folder_bd + "/" + "forums.bd")
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS discuss (
            id_subjet,
            name_user text,
            message_user text,
            publication_date text,
            publication_time text)""")
        subjet = cursor.execute(f"SELECT * FROM subjets_forums WHERE id_subjet='{id_subjet}'").fetchall()
        conn.commit()
        conn.close()

        frame_main = QtWidgets.QFrame()
        frame_main.setObjectName("frame_main")
        frame_main.setStyleSheet("""
            QFrame#frame_subjet{
            }
            
            QLabel#label_title {
                margin: 20px;
            }
            """)
        
        title_subjet = subjet[0][1]
        label_title = QtWidgets.QLabel(title_subjet, frame_main)
        label_title.setObjectName("label_title")
        font_title = QtGui.QFont()
        font_title.setFamily("Arial")
        font_title.setPointSize(24)
        font_title.setWeight(50)
        font_title.setBold(True)
        label_title.setFont(font_title)
        
        frame_subjet = QtWidgets.QFrame(frame_main)
        frame_subjet.adjustSize()
        frame_subjet.setObjectName("frame_subjet")
        frame_subjet.move(25, 100)
        
        label_picture_user = QtWidgets.QLabel(frame_subjet)
        label_picture_user.setGeometry(0, 25, 100, 100)
        picture_modify = QtGui.QPixmap(folder_img + "/" + "avatar_defaut.png")
        picture_modify =  picture_modify.scaled(100, 100)
        label_picture_user.setPixmap(picture_modify)

        label_name_user = QtWidgets.QLabel("Afri Kreto", frame_subjet)
        label_name_user.setObjectName("label_name_user")
        #label_name_user.setStyleSheet("border: 1px solid black; margin-bottom: 50px;")
        label_name_user.setFixedWidth(100)
        label_name_user.adjustSize()
        font = QtGui.QFont()
        font.setBold(True)
        font.setFamily("Arial")
        font.setPointSize(16)
        label_name_user.setFont(font)
        
        label_day = QtWidgets.QLabel("Jeudi 15 mars", frame_subjet)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        label_day.setFont(font)
        label_day.setObjectName("label_day")
        label_day.setStyleSheet("QLabel#label_day {color: #696969;}")
        label_day.adjustSize()
        label_day.move(120, 0)
        
        label_description = QtWidgets.QLabel(frame_subjet)
        label_description.setObjectName("label_description")
        label_description.setFixedWidth(450)
        font = QtGui.QFont()
        font.setFamily("Time New Roman")
        font.setPointSize(16)
        
        #label_description.setStyleSheet("border: 1px solid blck;")
        label_description.setText("""Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam id vestibulum lectus, quis aliquet lectus. Donec laoreet facilisis metus, id sagittis nisi placerat condimentum. Ut condimentum lectus ac luctus posuere. Mauris eu neque tortor. Duis in augue tempor, malesuada nibh eu, posuere mi. Integer dapibus ut nulla eu maximus. Proin ac libero finibus, porta erat quis, aliquet quam. Vivamus elit orci, placerat laoreet faucibus vitae, scelerisque a magna. Suspendisse interdum dui a leo ullamcorper imperdiet. Donec volutpat congue ante non placerat. Mauris accumsan non mauris eget congue. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Donec scelerisque interdum tellus nec congue. Etiam nec pharetra risus, vitae tempus metus. Curabitur id nisl laoreet, pellentesque urna a, ornare nulla. Fusce blandit, leo vel euismod porttitor, dolor magna dignissim justo, sed consectetur augue justo ac mi.

Etiam blandit ante non arcu fringilla fermentum. Vivamus vitae luctus diam. Nulla auctor feugiat lacinia. Morbi ac erat quam. Nam finibus lectus id lectus placerat sagittis. Phasellus vel gravida diam. Ut vitae lorem commodo dolor dictum tincidunt ac suscipit ipsum. Nulla pharetra sem euismod pretium volutpat. Quisque placerat tincidunt dolor at placerat. Nullam ornare viverra tempor. Donec congue tincidunt leo in faucibus. Phasellus tristique sed odio sed porta. Morbi et est risus. Vestibulum eget odio pellentesque, tempor felis eget, tempor ante.

Nulla tempus enim sapien, at rhoncus dui scelerisque quis. Vestibulum accumsan pharetra ultrices. Maecenas a lorem quam. Proin tincidunt est libero, eget tempor arcu lobortis sed. In facilisis malesuada nibh vitae maximus. Etiam elementum elit ipsum, eu venenatis risus finibus quis. Donec ac massa finibus, dignissim ipsum luctus, tristique felis. Ut eu facilisis ex. Proin in diam in dui blandit iaculis. Ut sit amet finibus tellus, nec condimentum enim. Fusce sodales tincidunt tortor nec egestas. Vestibulum fermentum eros egestas justo accumsan, vitae feugiat erat interdum. Etiam consectetur urna sit amet libero semper vestibulum.

Nunc porttitor tellus nec lorem dignissim tincidunt. Suspendisse quis quam dignissim, tempus mi dictum, consequat erat. Duis est eros, porttitor at urna luctus, eleifend venenatis turpis. Praesent viverra ornare blandit. Nunc lacinia felis et nisi sollicitudin, id ornare velit posuere. In nisi ex, gravida sed ligula vel, blandit hendrerit libero. Nullam ut sem nec nisl ultrices tincidunt. Aenean tortor ex, congue vitae ultricies a, luctus ut magna. Sed suscipit sodales lacus, quis condimentum eros ultricies et. Pellentesque iaculis mi non risus eleifend facilisis. In ultricies convallis vehicula. Aenean tortor dui, pharetra sit amet lorem a, iaculis imperdiet velit. Donec luctus quis est vitae tempor. Aenean et nulla odio. Donec luctus in purus et sagittis.

Sed eleifend metus quis consectetur volutpat. Suspendisse pretium justo velit, eget fringilla odio ultrices ac. Ut eu maximus dui. Sed laoreet diam eget leo luctus hendrerit. In luctus, purus varius ornare finibus, sapien velit ultricies lorem, nec semper felis leo sit amet libero. Sed ut porttitor nunc, at accumsan purus. Nunc ut risus dictum, molestie dolor vitae, dapibus arcu. Quisque ac ultricies dolor. Ut porttitor nibh vel dui porttitor porttitor. Proin purus lectus, euismod rutrum turpis eget, sagittis consequat tortor.

Proin tempus a sapien et blandit. Cras auctor suscipit facilisis. Pellentesque varius aliquet tincidunt. Fusce venenatis rhoncus nibh, nec ornare ligula fermentum id. Suspendisse potenti. Curabitur ultrices nec tellus et lacinia. Mauris nec nulla at velit varius finibus. Quisque sodales euismod ligula. Nam ac cursus lacus. Sed ut arcu cursus tellus ultrices tristique. Donec sed erat ut lectus aliquet vestibulum blandit quis risus. Duis convallis tempus hendrerit. Cras id pulvinar felis, ac pellentesque mauris. Nulla sed mi et lectus cursus suscipit sagittis vitae erat.

Nullam vel ullamcorper sapien, et ornare libero. Suspendisse dapibus arcu turpis, nec auctor enim volutpat non. Nam gravida est eu ante lobortis, ut ultricies augue porttitor. Vestibulum accumsan vitae augue eu iaculis. Aenean pretium maximus mollis. Donec convallis consequat mi, ut sodales arcu facilisis eget. Nam lacus mauris, condimentum et libero non, rutrum condimentum turpis. Fusce et congue nunc. In lacinia sit amet nibh ut bibendum. Nulla semper interdum neque, ut varius ipsum pellentesque eu. Etiam placerat feugiat aliquet. Pellentesque in sodales sapien.

Donec eget sapien et quam posuere vestibulum eu id massa. Maecenas justo odio, tempor sit amet iaculis id, mattis eget ante. Suspendisse ultricies vitae orci quis fermentum. Aenean ultrices sapien augue, id finibus libero molestie non. Donec pulvinar turpis id luctus efficitur. Suspendisse lobortis scelerisque odio at pulvinar. Donec odio purus, egestas nec cursus id, commodo sit amet turpis. In hac habitasse platea dictumst. Nam sagittis velit sit amet dolor maximus, ut fermentum turpis finibus. Proin dapibus libero ac sapien sollicitudin dapibus. Nulla mattis accumsan mi at tincidunt. Sed sed porta justo, at ullamcorper nulla. Praesent dolor libero, viverra quis ex vitae, porta hendrerit sapien.

Aenean quis sem ut diam congue ultrices. Vivamus luctus sapien nec velit consectetur, et bibendum nisl gravida. Integer non faucibus tellus, nec vehicula felis. Morbi dolor eros, congue in dictum a, molestie blandit ante. Suspendisse potenti. Maecenas blandit nibh pulvinar sem gravida, in congue lacus pharetra. Cras sed porttitor quam. Fusce sagittis nulla et augue feugiat elementum. Maecenas non dictum ante, nec suscipit ipsum. Sed facilisis risus at risus convallis auctor. Nam a arcu posuere, commodo felis sit amet, egestas leo. Duis luctus lacus sed venenatis dictum. Etiam auctor tortor in risus rutrum, et fringilla metus dignissim. Fusce sit amet velit vestibulum, eleifend odio vitae, consequat nunc. Pellentesque nisi risus, pulvinar in felis eget, facilisis tempor metus.

Suspendisse risus velit, lacinia ac augue sit amet, malesuada aliquam sem. Vivamus dictum rhoncus facilisis. Nunc ut facilisis tortor. Etiam lacinia neque eu mauris dictum, vel dictum ex tristique. Ut at dapibus dolor. Vestibulum mollis dui ac augue egestas fringilla. Proin venenatis mi turpis, vel laoreet nibh posuere ac. Proin posuere nisi at lorem ultricies, a tempus nunc ullamcorper. Cras urna purus, malesuada a convallis a, pulvinar id felis. Proin felis sem, condimentum efficitur ullamcorper quis, porttitor sit amet tortor. Maecenas sed dapibus nunc, a viverra nisl. Fusce sit amet nunc aliquet metus dictum mollis. Pellentesque eget rhoncus tellus, et commodo libero.""")
        label_description.setWordWrap(True)
        label_description.adjustSize()
        label_description.setAlignment(QtCore.Qt.AlignLeft)
        label_description.move(120, 30)
        font = QtGui.QFont()
        font.setFamily("Time New Roman")
        font.setPointSize(14)
        label_description.setFont(font)
        self.vbox_2.addWidget(frame_main)
        
        # for i in range(0, 51):
        #     label = QtWidgets.QLabel("Label discussion")
        #     self.vbox_2.addWidget(label)
            
        self.discuss.setLayout(self.vbox_2)
        
        #Scroll Area Properties
        self.contenai_discuss.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.contenai_discuss.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.contenai_discuss.setWidgetResizable(True)
        self.contenai_discuss.setWidget(self.discuss)
        
    def recording_user(self):
        # Récupératioin des données saisir pas l'utilisateur
        last_name = self.enter_last_name.text()
        first_name = self.enter_first_name.text()
        email = self.enter_email.text()
        gender = self.enter_gender.currentText()
        clas = self.enter_class.currentText()
        password_1 = self.enter_password_1.text()
        password_2 = self.enter_password_2.text()
        
        if (last_name and first_name and email and gender and clas and password_1 == password_2
            and last_name.isalpha() and first_name.isalpha() and not last_name.isspace()
            and not first_name.isspace() and not email.isspace() and not password_1.isspace() and not password_2.isspace()):
            msg_user = """
            Vous venez de recevoir un code validation dans vôtre boite mail.
            Veuillez le saisit pour valider vôtre inscription.
            """
            self.d = {
                "last_name": last_name, 
                "first_name": first_name,
                "email": email,
                "gender": gender,
                "class": clas,
                "password": password_1
            }
            self.code = self.email_confimed(last_name, email)
            QMessageBox.about(self, "Code de validation", msg_user)
            self.stackedWidget.setCurrentWidget(self.page_confimed_code)     
        else:
            QMessageBox.about(self, "Erreur", "Une erreur est survenue lors de l'enregistrement, Veuillez vérifier vos informations")
       
    def recording_final(self):
        code_user = self.enter_code.text()
        if code_user == self.code:
            conn = sqlite3.connect(folder_bd + "/" + "etudiants.bd")
            cursor = conn.cursor()
            cursor.execute(f"""CREATE TABLE IF NOT EXISTS etudiants(
                last_name text,
                first_name text,
                email text,
                gender text,
                class text,
                password text) """)
            cursor.execute("""INSERT INTO etudiants VALUES (:last_name, 
                :first_name,
                :email,
                :gender,
                :class,
                :password)""", self.d)
            conn.commit()
            conn.close()
            QMessageBox.about(self, "Code valide", "Félicitation Vous venez de valider vôtre inscription")
            self.window_subjets()
        else: QMessageBox.about(self, "Code invalide", "Le code que vous avez saisit est invalide")
            
    def email_confimed(self, name_user, email_user):
        code = []
        list_number = string.digits
        
        for i in range(0, 6): 
            n = choice(list_number) 
            code.append(n)
        code = "".join(code)
         
        msg = """subject: Validation de l'inscription\n
        Félicitation {} vous venez de vous inscrit sur l'application ChatSchool.
        Pour valider vôtre inscription veuillez entrer le code suivant: {}
        """.format(name_user, code)
        msg = msg.encode("utf-8")
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login("chatschool22@gmail.com", "Popo2022")
        server.sendmail("chatschool22@gmail.com", email_user, msg)
        server.quit()
        
        return code

    def get_data(self, name_file, name_table):
        FILE = folder_bd + "/" + name_file
        conn = sqlite3.connect(FILE)
        cursor = conn.cursor()
        data = cursor.execute(f"SELECT * FROM subjets_forums").fetchall()
        conn.commit()
        conn.close()
        return data

    def generation_id_subjet(self):
        list_subjet_forums = self.get_data("forums.bd", "subjets_forums")
        code = []
        list_number = string.digits
        
        for i in range(0, 6): 
            n = choice(list_number) 
            code.append(n)
        code = "".join(code)
        
        for forums in list_subjet_forums:
            code_exists = forums[3]
            if code_exists == code:
                return self.generation_id_subjet()
        return code
        
    def recording_sujet(self):
        subjet = self.enter_subjet.currentText().lower()
        title = self.enter_title_subjet.text()
        description = self.enter_description.toPlainText()

        # Le programme récupère la date d'aujoud'hui        
        date_recording = self.date_recording_subjet()
        d = {
            "subjet": subjet,
            "title": title,
            "description": description,
            "author": "user user",
            "date_day": date_recording.get("day"),
            "date_time": date_recording.get("time"),
            "id_subjet": None
        }

        if subjet and title and description and not subjet.isspace() and not title.isspace() and not description.isspace():
            conn = sqlite3.connect(folder_bd + "/" + "forums.bd")
            cursor = conn.cursor()
            cursor.execute(f"""CREATE TABLE IF NOT EXISTS subjets_forums(
            subjet text,
            title text,
            description text,
            author text,
            date_day text,
            date_time text,
            id_subjet text)""")
            id_subjet = self.generation_id_subjet()
            d["id_subjet"] = id_subjet 
            cursor.execute(f"""INSERT INTO subjets_forums VALUES (
            :subjet,
            :title,
            :description,
            :author,
            :date_day,
            :date_time,
            :id_subjet)""", d)
            conn.commit()
            conn.close()        
            QMessageBox.about(self, "Sujet", "Vôtre sujet vient d'être publié")    
        else: QMessageBox.about(self, "Imposible d'ajouter le sujet", "Une erreur est survenue lors de l'ajout du sujet, Veuillez vérifier les données les données que vous avez saisit")

    def date_recording_subjet(self):
        today = datetime.now()
        day = today.strftime("%Y/%m/%d")
        time = today.strftime("%H:%M:%S")
        date = {"day": day, "time": time}
        return date

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1021, 703)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Vbox display subjet
        self.vbox = QtWidgets.QVBoxLayout()
        
        # Vbox display subjet
        self.vbox_2 = QtWidgets.QVBoxLayout()
        
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(310, 0, 711, 671))
        self.stackedWidget.setStyleSheet("")
        self.stackedWidget.setObjectName("stackedWidget")
        
        self.page_confimed_code = QtWidgets.QWidget()
        self.page_confimed_code.setObjectName("page_confimed_code")
        self.page_confimed_code.setStyleSheet("""QWidget#page_confimed_code {
            background-color: white;}""")
        self.label_code = QtWidgets.QLabel("Entrer le code", self.page_confimed_code)
        self.label_code.setObjectName("label_code")
        self.label_code.setGeometry(270, 300, 331, 31)
        font = QtGui.QFont("Arial", 18)
        self.label_code.setFont(font)
        self.enter_code = QtWidgets.QLineEdit(self.page_confimed_code) 
        self.enter_code.setGeometry(200, 350, 300, 35)
        self.enter_code.setFont(QtGui.QFont("Times New Roman", 14))
        self.enter_code.setObjectName("enter_code")
        self.enter_code.setStyleSheet("""QLineEdit#enter_code {
            background-color: rgb(236, 236, 236);
            border-radius: 3px;
            padding: 5px;
            border: 1px solid rgb(160, 161, 182);
            border-left: 0px;
            border-right: 0px;
            border-top: 0px;
        }
        
        QLineEdit#enter_code::hover {
            border-bottom-color: rgb(64, 40, 200);
        }
        """)
        
        self.bnt_code = QtWidgets.QPushButton("Valider", self.page_confimed_code)
        self.bnt_code.clicked.connect(self.recording_final)
        self.bnt_code.setGeometry(280, 400, 150, 35)
        self.bnt_code.setFont(QtGui.QFont("Arial", 14))
        self.bnt_code.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bnt_code.setObjectName("bnt_code")
        self.bnt_code.setStyleSheet("""QPushButton#bnt_code{
            background-color: white;
            color: rgb(2, 171, 0);
            padding: 5px;
            border: 2px solid rgb(2, 171, 0);
            border-radius: 5px;
        }
        
        QPushButton#bnt_code::hover{
            background-color: rgb(2, 171, 0);
            color: white;
        }
        """)
        self.stackedWidget.addWidget(self.page_confimed_code)
        
        # Page création de la discution
        self.page_creat_discuss = QtWidgets.QWidget()
        self.page_creat_discuss.setObjectName("page_creat_discuss")
        self.page_creat_discuss.setStyleSheet("""QWidget#page_creat_discuss {
        background-color: white;}""")
        
        
        self.frame_creat_subjet = QtWidgets.QFrame(self.page_creat_discuss)
        self.frame_creat_subjet.setObjectName("frame_creat_subjet")
        self.frame_creat_subjet.setGeometry(100, 100, 450, 450)
        self.frame_creat_subjet.setStyleSheet("""QFrame#frame_creat_subjet{
            border: 1px solid black;
            }""")
        
        self.enter_subjet = QtWidgets.QComboBox(self.frame_creat_subjet)
        self.enter_subjet.setGeometry(100, 100, 331, 24)
        self.enter_subjet.setObjectName("enter_subjet")
        self.enter_subjet.setStyleSheet("QComboBox#enter_subjet {\n"
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
        
        list_subjet = ["SVT", "Physique", "Anglais", "Philosophie"]
        for item in list_subjet: self.enter_subjet.addItem(item)
        
        self.enter_title_subjet = QtWidgets.QLineEdit(self.frame_creat_subjet)
        self.enter_title_subjet.setGeometry(100, 150, 331, 28)
        self.enter_title_subjet.setObjectName("enter_title_subjet")
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.enter_title_subjet.setFont(font)
        self.enter_title_subjet.setStyleSheet("QLineEdit#enter_title_subjet{\n"
"background-color: rgb(236, 236, 236);\n"
"border-radius: 3px;\n"
"padding: 5px;\n"
"border: 1px solid rgb(160, 161, 182);\n"
"border-left: 0px;\n"
"border-right: 0px;\n"
"border-top: 0px;\n"
"}\n"
"\n"
"QLineEdit#enter_title_subjet::hover {\n"
"border-bottom-color: rgb(64, 40, 200);\n"
"\n"
"}")
        
        self.enter_description = QtWidgets.QTextEdit(self.frame_creat_subjet)
        self.enter_description.setGeometry(100, 200, 331, 150)
        
        self.bnt_creat_subjet = QtWidgets.QPushButton("Crée le sujet", self.frame_creat_subjet)
        self.bnt_creat_subjet.clicked.connect(self.recording_sujet)
        self.bnt_creat_subjet.setObjectName("bnt_creat_subjet")
        self.bnt_creat_subjet.setGeometry(230, 370, 200, 31)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(14)
        self.bnt_creat_subjet.setFont(font)
        self.bnt_creat_subjet.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bnt_creat_subjet.setStyleSheet("QPushButton#bnt_creat_subjet{"
"background-color: white;"
"color: rgb(2, 171, 0);"
"padding: 5px;"
"border: 2px solid rgb(2, 171, 0);"
"border-radius: 5px;"
"}"
""
""
"QPushButton#bnt_creat_subjet::hover{"
"background-color: rgb(2, 171, 0);"
"color: white;"
"}"
"")
        
        self.stackedWidget.addWidget(self.page_creat_discuss)
        
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
        self.bnt_connection.setStyleSheet("QPushButton#bnt_connection{"
"background-color: white;"
"color: rgb(64, 40, 200);"
"padding: 5px;"
"border: 2px solid rgb(64, 40, 200);"
"border-radius: 5px;"
"}"
""
""
"QPushButton#bnt_connection::hover{"
"background-color: rgb(64, 40, 200);"
"color: white;"
"}"
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
        self.bnt_subcription.clicked.connect(self.recording_user)
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
"border-bottom-color: rgb(64, 40, 200);\n"
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
        self.enter_gender.addItem("Homme")
        self.enter_gender.addItem("Femme")
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
        list_class = ["6éme", "5éme", "4éme", "3éme", "2nd", "1ère", "Terminal"]
        for item in list_class: self.enter_class.addItem(item)
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
        self.frame_category_4 = Frame(self.bar_nav)
        self.frame_category_4.clicked.connect(partial(self.window_subjets, "philosophie"))
        self.frame_category_4.setGeometry(QtCore.QRect(10, 370, 311, 71))
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
        
        # Frame ajout un sujet
        self.frame_reply = Frame(self.bar_nav)
        self.frame_reply.clicked.connect(self.window_creat_subjet)
        self.frame_reply.setGeometry(QtCore.QRect(10, 450, 311, 80))
        self.frame_reply.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.frame_reply.setStyleSheet("QFrame#frame_reply::hover{\n"
"background-color: rgb(204, 204, 204);\n"
"}")
        self.frame_reply.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_reply.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_reply.setObjectName("frame_reply")
        self.label_subjet = QtWidgets.QLabel(self.frame_reply)
        self.label_subjet.setGeometry(QtCore.QRect(110, 31, 131, 32))
        self.label_subjet.setText("Créé un sujet")
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(16)
        font.setWeight(75)
        self.label_subjet.setFont(font)
        self.label_subjet.setObjectName("label_subjet")
        self.label_img_subjet = QtWidgets.QLabel(self.frame_reply)
        self.label_img_subjet.setGeometry(QtCore.QRect(16, 10, 71, 70))
        self.label_img_subjet.setPixmap(QtGui.QPixmap("D:\Programmation\Documents\Projet_Nan\education\img\groupe-de-discussion.png"))
        self.label_img_subjet.setScaledContents(True)
        self.label_img_subjet.setObjectName("label_img_subjet")
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

        self.frame_category_2 = Frame(self.bar_nav)
        self.frame_category_2.clicked.connect(partial(self.window_subjets, "physique"))
        self.frame_category_2.setGeometry(QtCore.QRect(30, 171, 311, 61))
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
        self.frame_category_3 = Frame(self.bar_nav)
        self.frame_category_3.clicked.connect(partial(self.window_subjets, "svt"))
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
        self.logo.setPixmap(QtGui.QPixmap("UI\\../img/planète-terre.png"))
        self.logo.setScaledContents(True)
        self.logo.setObjectName("logo")
        self.label_matiere_litraire = QtWidgets.QLabel(self.bar_nav)
        self.label_matiere_litraire.setGeometry(QtCore.QRect(50, 260, 151, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.label_matiere_litraire.setFont(font)
        self.label_matiere_litraire.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.label_matiere_litraire.setObjectName("label_matiere_litraire")
        self.frame_category_6 = Frame(self.bar_nav)
        self.frame_category_6.clicked.connect(partial(self.window_subjets, "anglais"))
        self.frame_category_6.setGeometry(QtCore.QRect(10, 300, 311, 61))
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
        self.enter_title_subjet.setPlaceholderText(_translate("MainWindow", "Entrer le titre du subjet"))
        self.label_subscription.setText(_translate("MainWindow", "Inscription"))
        self.lien_connection.setText(_translate("MainWindow", "Connecter vous ici"))
        self.label_unitile_2.setText(_translate("MainWindow", "Vous avez déha un compte ?"))
        self.label_connection.setText(_translate("MainWindow", "Connection"))
        self.label.setText(_translate("MainWindow", "Forums"))
        self.label_matire_scientifique.setText(_translate("MainWindow", "Matiére scientifique"))
        self.label_9.setText(_translate("MainWindow", "Philosophie"))
        self.label_7.setText(_translate("MainWindow", "Physique"))
        self.label_8.setText(_translate("MainWindow", "SVT"))
        self.label_matiere_litraire.setText(_translate("MainWindow", "Matiére litéraire"))
        self.label_11.setText(_translate("MainWindow", "Anglais"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
