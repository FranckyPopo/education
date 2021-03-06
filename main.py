# -*- coding: utf-8 -*-
from itertools import count
import os
import sqlite3
import sys
import string
import smtplib
from random import choice
from functools import partial
from datetime import datetime
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
    count = 1
    def __init__(self):
        super().__init__()
        self.setGeometry(500, 250, 714, 672)
        self.setFixedSize(1000, 700)
        self.setupUi(self)
        self.window_subjets("svt")
        self.user_connection = False
        self.idenfiant_user = None
        
    def window_connection(self):
        if self.user_connection:
            self.msgQuestion = QMessageBox()
            self.msgQuestion.setIcon(QMessageBox.Question)
            self.msgQuestion.setText("Voulez-vous vous déconnecter ?")
            self.msgQuestion.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            self.msgQuestion.buttonClicked.connect(self.deconnection_user)
            self.msgQuestion.setWindowTitle("Déconnection")
            self.msgQuestion.show() 
        else:
            self.stackedWidget.setCurrentWidget(self.page_connection)
        
    def window_subscription(self):
        self.stackedWidget.setCurrentWidget(self.page_subscription)
        
    def window_subjets(self, name_subjet: str):
        self.stackedWidget.setCurrentWidget(self.page_subjet)
        self.display_subjet(name_subjet)
        
    def window_creat_subjet(self):
        self.stackedWidget.setCurrentWidget(self.page_creat_discuss)
        
    def window_discuss(self, id_subject):
        self.stackedWidget.setCurrentWidget(self.page_discuss)
        self.display_dicuss(id_subject)
        
    def decorator(func):
        def connection(self, id_subjet):
            if self.user_connection:
                return func(self, id_subjet)
            else:
                QMessageBox.about(self, "Imposible de publié un message erreur", "Vous devez vous connecter avant de publier une réponse")
        return connection
  
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
            id_subject = subjet[6]
            
            frame_subjet = Frame()
            frame_subjet.clicked.connect(partial(self.window_discuss, id_subject))
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
            day = subjet[4]
            author = subjet[3]
            infos = f"Par {author} {day}"
            
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

    def display_dicuss(self, id_subject):
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
        subject = cursor.execute(f"SELECT * FROM subjets_forums WHERE id_subjet='{id_subject}'").fetchall()
        conn.commit()
        conn.close()
        
        author = subject[0][3]
        date_day = subject[0][4]
        description = subject[0][2]

        frame_main = QtWidgets.QFrame()
        frame_main.setFixedSize(700, 200)
        frame_main.setObjectName("frame_main")
        frame_main.setStyleSheet("QFrame#frame_main::hover {background-color: #C0C0C0;}")
        
        title_subjet = subject[0][1]
        label_title = QtWidgets.QLabel(title_subjet)
        label_title.setFixedSize(700, 80)
        label_title.move(50, 0)
        
        label_title.setObjectName("label_title")
        font_title = QtGui.QFont()
        font_title.setFamily("Arial")
        font_title.setPointSize(24)
        font_title.setBold(True)
        label_title.setFont(font_title)
        
        label_picture_user = QtWidgets.QLabel(frame_main)
        label_picture_user.move(20, 30)
        picture_modify = QtGui.QPixmap(os.path.join(folder_img, "avatar_defaut.png"))
        picture_modify =  picture_modify.scaled(100, 100)
        label_picture_user.setPixmap(picture_modify)

        label_name_user = QtWidgets.QLabel(author, frame_main)
        label_name_user.move(20, 0)
        label_name_user.setObjectName("label_name_user")
        
        label_name_user.setFixedWidth(100)
        label_name_user.adjustSize()
        font = QtGui.QFont()
        font.setBold(True)
        font.setFamily("Arial")
        font.setPointSize(16)
        label_name_user.setFont(font)
        
        label_day = QtWidgets.QLabel(date_day, frame_main)
        label_day.move(150, 0)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        label_day.setFont(font)
        label_day.setObjectName("label_day")
        label_day.setStyleSheet("QLabel#label_day {color: #696969;}")
        label_day.adjustSize()
        
        label_description = QtWidgets.QLabel(frame_main)
        label_description.setObjectName("label_description")
        label_description.move(150, 30)
        label_description.setFixedWidth(500)
        font = QtGui.QFont()
        font.setFamily("Time New Roman")
        font.setPointSize(16)
        label_description.setFont(font)

        label_description.setText(description)
        label_description.setWordWrap(True)
        label_description.adjustSize()
        label_description.setAlignment(QtCore.Qt.AlignLeft)
        
        self.vbox_2.addWidget(label_title)
        self.vbox_2.addWidget(frame_main)

        conn = sqlite3.connect(folder_bd + "/" + "forums.bd")
        cursor = conn.cursor()
        discuss = cursor.execute(f"SELECT * FROM discuss WHERE id_subjet='{id_subject}'").fetchall()
        conn.commit()
        conn.close()
        
        for item in discuss:
            name = item[1]
            message = item[2]
            date = item[3]

            frame_reply = QtWidgets.QFrame()
            frame_reply.setFixedSize(700, 200)
            frame_reply.setObjectName("frame_reply")
            frame_reply.setStyleSheet("""
                QFrame#frame_reply{
                    margin-top: 20px;
                    margin-bottom: 20px;
                }
            """)
            
            if MainWindow.count % 2 == 0:
                frame_reply.setStyleSheet("""
                QFrame#frame_reply{
                    background-color: #ececec;
                }
                QFrame#frame_reply::hover{
                    background-color: #C0C0C0;
                }""")
            else:
                 frame_reply.setStyleSheet("""
                QFrame#frame_reply::hover{
                    background-color: white;
                }
                
                QFrame#frame_reply::hover{
                    background-color: #C0C0C0;
                }""")
            MainWindow.count += 1
            
            label_picture_user = QtWidgets.QLabel(frame_reply)
            label_picture_user.move(20, 30)
            picture_modify = QtGui.QPixmap(os.path.join(folder_img, "avatar_defaut.png"))
            picture_modify =  picture_modify.scaled(100, 100)
            label_picture_user.setPixmap(picture_modify)
            
            label_name_user = QtWidgets.QLabel(name, frame_reply)
            label_name_user.move(20, 0)

            font.setBold(True)
            font.setFamily("Arial")
            font.setPointSize(16)
            label_name_user.setFont(font)
            
            label_day = QtWidgets.QLabel(date, frame_reply)
            label_day.move(150, 0)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(16)
            label_day.setFont(font)
            label_day.setObjectName("label_day")
            label_day.setStyleSheet("QLabel#label_day {color: #696969;}")
            label_day.adjustSize()
            
            label_description = QtWidgets.QLabel(frame_reply)
            label_description.setObjectName("label_description")
            #label_description.setStyleSheet("border: 1px solid black;")
            label_description.move(150, 30)
            label_description.setFixedWidth(500)
            font = QtGui.QFont()
            font.setFamily("Time New Roman")
            font.setPointSize(16)
            label_description.setFont(font)

            description = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam id vestibulum lectus, quis aliquet lectus. Donec laoreet facilisis metus, id sagittis nisi placerat condimentum. Ut condimentum lectus ac luctus posuere. Mauris eu neque tortor. Duis in augue tempor, ok"""
            label_description.setText(message)
            label_description.setWordWrap(True)
            label_description.adjustSize()
            label_description.setAlignment(QtCore.Qt.AlignLeft)
            
            self.vbox_2.addWidget(frame_reply)
            
        self.enter_message = QtWidgets.QTextEdit()
        self.enter_message.setFixedSize(680, 170)
        self.enter_message.setObjectName("enter_message")
        self.enter_message.setStyleSheet("""
            QTextEdit#enter_message{
                border-radius: 2px;
                border: 1px solid black;
                font-size: 14px;
                font-family: Time New Roman;
                margin-left: 10px; 
                margin-bottom: 10px; 
                padding: 5px;
            }
            
            QTextEdit#enter_message:focus {
                border-color: blue;
            }
            """)
        
        bnt_reply_message = QtWidgets.QPushButton("Répondre")
        bnt_reply_message.clicked.connect(partial(self.reply_subjet, id_subject))
        bnt_reply_message.setObjectName("bnt_reply_message")
        bnt_reply_message.setStyleSheet("""
            QPushButton#bnt_reply_message{
                margin-left: 570px;
                font-size: 16px;
                font-weight: bold;
                background-color: white;
                color: blue;
                border-radius: 3px;
                border: 1px solid blue;
            }
            
            QPushButton#bnt_reply_message::hover{
                background-color: blue;
                color: white;
            }
        """)
        bnt_reply_message.setFixedSize(680, 30)
        
        self.vbox_2.addWidget(self.enter_message)
        self.vbox_2.addWidget(bnt_reply_message)
        self.discuss.setLayout(self.vbox_2)
        
        #Scroll Area Properties
        self.contenai_discuss.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.contenai_discuss.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.contenai_discuss.setWidgetResizable(True)
        self.contenai_discuss.setWidget(self.discuss)
      
    @decorator
    def reply_subjet(self, id_subject):
        # Le programme récupère les données de l'utilisateur
        date = self.date_recording_subjet()
        d = {
            "id_subject": id_subject,
            "user_name": f"{self.idenfiant_user[1]} {self.idenfiant_user[0]}",
            "message_user": self.enter_message.toPlainText(),
            "date_day": date["day"],
            "date_time": date["time"]
        }
        
        message_user = self.enter_message.toPlainText()
        if message_user and not message_user.isspace():
            conn = sqlite3.connect(folder_bd + "/" + "forums.bd")
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO discuss 
                VALUES (:id_subject,
                :user_name,
                :message_user,
                :date_day,
                :date_time
                )""", d)
            conn.commit()
            conn.close()
            QMessageBox.about(self, "Message publié", "Vôtre message vient d'être publié")
            self.display_dicuss(id_subject)
        else: QMessageBox.about(self, "Imposible de publié un message erreur", "Vous devez remplir le champ avant d'envoyer la réponse")
         
    def deconnection_user(self, i):
        if i.text() == '&Yes' :
            self.user_connection = False
            self.label_connection.setText("Connection")
            QMessageBox.about(self, "Déconnection", "Vous venez de vous déconnecter")
              
    def account_verification(self, email_student: str) -> bool:    
        students = self.get_data("etudiants.bd", "etudiants")
        for student in students:
            if student[2] == email_student:
                return True
        return False
     
    def recording_user(self):
        # Récupératioin des données saisir pas l'utilisateur
        self.last_name = self.enter_last_name.text()
        self.first_name = self.enter_first_name.text()
        self.email = self.enter_email.text()
        self.gender = self.enter_gender.currentText()
        self.clas = self.enter_class.currentText()
        self.password_1 = self.enter_password_1.text()
        password_2 = self.enter_password_2.text()
        
        account_exists = self.account_verification(self.email)
        if account_exists:
            QMessageBox.about(self, "Compte", "L'email que vous avez saisit est associé a un compte")
        else:
            if (self.last_name and self.first_name and self.email and self.gender and self.clas and self.password_1 == password_2
                and self.last_name.isalpha() and self.first_name.isalpha() and not self.last_name.isspace()
                and not self.first_name.isspace() and not self.email.isspace() and not self.password_1.isspace() and not password_2.isspace()):
                msg_user = """
                Vous venez de recevoir un code validation dans vôtre boite mail.
                Veuillez le saisit pour valider vôtre inscription.
                """
                self.d = {
                    "last_name": self.last_name, 
                    "first_name": self.first_name,
                    "email": self.email,
                    "gender": self.gender,
                    "class": self.clas,
                    "password": self.password_1
                }
                self.code = self.email_confimed(self.last_name, self.email)
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
            
            self.user_connection = True
            self.idenfiant_user = (self.last_name, self.first_name, self.email , self.gender, self.clas, self.password_1)
            self.label_connection.setText(f"{self.first_name} {self.last_name}")
            
            # Suppréssion des valeurs des entrés
            self.enter_last_name.clear()
            self.enter_first_name.clear()
            self.enter_email.clear()
            self.enter_password_1.clear()
            self.enter_password_2.clear()
            self.enter_code.clear()
            
            self.window_subjets("svt")
            QMessageBox.about(self, "Code valide", "Félicitation Vous venez de valider vôtre inscription")
        else: QMessageBox.about(self, "Code invalide", "Le code que vous avez saisit est invalide")
            
    def connection_user(self):
        # Récupération des données de l'utilisateur
        email = self.enter_email_connection.text()
        password = self.enter_password_connection.text()
        students = self.get_data("etudiants.bd", "etudiants")
        
        for student in students:
            if student[2] == email and student[5] == password:
                QMessageBox.about(self, "Connection réussite", "Vous être désormais connecté")
                self.user_connection = True
                self.idenfiant_user = student
                self.label_connection.setText(f"{self.idenfiant_user[1]} {self.idenfiant_user[0]}")
                self.window_subjets("svt")
                self.enter_email_connection.clear()
                self.enter_password_connection.clear()
                break
        else:
            QMessageBox.about(self, "Connection impossible", "Identifiant incorrect")
            
    def email_confimed(self, name_user: str, email_user: str) -> list:
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
        server.login("chatschool22@gmail.com", "compteN03")
        server.sendmail("chatschool22@gmail.com", email_user, msg)
        server.quit()
        
        return code

    def get_data(self, name_file: str, name_table: str) -> list:
        FILE = folder_bd + "/" + name_file
        conn = sqlite3.connect(FILE)
        cursor = conn.cursor()
        data = cursor.execute(f"SELECT * FROM {name_table}").fetchall()
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
    
    @decorator
    def recording_sujet(self, none: None) -> None:
        subjet = self.enter_subjet.currentText().lower()
        title = self.enter_title_subjet.text()
        description = self.enter_description.toPlainText()

        # Le programme récupère la date d'aujoud'hui        
        date_recording = self.date_recording_subjet()

        d = {
            "subjet": subjet,
            "title": title,
            "description": description,
            "author": f"{self.idenfiant_user[1]} {self.idenfiant_user[0]}",
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
            self.window_discuss(id_subjet)
            self.enter_title_subjet.clear()  
            self.enter_description.clear()
        else: QMessageBox.about(self, "Imposible d'ajouter le sujet", "Une erreur est survenue lors de l'ajout du sujet, Veuillez vérifier les données que vous avez saisit")

    def date_recording_subjet(self):
        today = datetime.now()        
        day = datetime.strftime(today, "%A %d %B %Y %H:%M:%S")
        time = datetime.strftime(today, "H:%M:%S")
        return {"day": day, "time": time}

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
        
        self.enter_subjet = QtWidgets.QComboBox(self.frame_creat_subjet)
        self.enter_subjet.setGeometry(20, 90, 400, 35)
        self.enter_subjet.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.enter_subjet.setObjectName("enter_subjet")
        self.enter_subjet.setStyleSheet("""
            QComboBox#enter_subjet {
                color: black;
                border-left: 0px; 
                border-top: 0px; 
                border-right: 0px;
                border-radius: 3px; 
                border-bottom: 1px solid rgb(204, 204, 204); 
                background-color: rgb(236, 236, 236); 
                padding: 10px;
                font-size: 14px;
            }
                
            QComboBox#enter_gender::hover {
                border-bottom-color: rgb(160, 161, 182);
            }
        """)
                    
        list_subjet = ["SVT", "Physique", "Anglais", "Philosophie"]
        for item in list_subjet: self.enter_subjet.addItem(item)
        
        self.enter_title_subjet = QtWidgets.QLineEdit(self.frame_creat_subjet)
        self.enter_title_subjet.setGeometry(20, 150, 400, 35)
        self.enter_title_subjet.setObjectName("enter_title_subjet")
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.enter_title_subjet.setFont(font)
        self.enter_title_subjet.setStyleSheet("""
            QLineEdit#enter_title_subjet{
                background-color: rgb(236, 236, 236);
                border-radius: 3px;
                padding: 5px;
                border: 1px solid rgb(160, 161, 182);
                border-left: 0px;
                border-right: 0px;
                border-top: 0px;
                font-size: 18px;
            }
            
            QLineEdit#enter_title_subjet::hover {
                border-bottom-color: rgb(64, 40, 200);
            }""")
        
        self.enter_description = QtWidgets.QTextEdit(self.frame_creat_subjet)
        self.enter_description.setGeometry(20, 200, 400, 150)
        self.enter_description.setObjectName("enter_description")
        self.enter_description.setStyleSheet("""
            QTextEdit#enter_description {
                border: 1px solid rgb(86, 84, 84); 
                border-radius: 3px;
                font-size: 14px;
            }
            
             QTextEdit#enter_description:focus {
                border-color: rgb(2, 171, 0);
            }
        """)
        
        self.bnt_creat_subjet = QtWidgets.QPushButton("Crée le sujet", self.frame_creat_subjet)
        self.bnt_creat_subjet.clicked.connect(self.recording_sujet)
        self.bnt_creat_subjet.setObjectName("bnt_creat_subjet")
        self.bnt_creat_subjet.setGeometry(250, 370, 170, 31)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(14)
        self.bnt_creat_subjet.setFont(font)
        self.bnt_creat_subjet.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bnt_creat_subjet.setStyleSheet("""
            QPushButton#bnt_creat_subjet {
                background-color: white;
                color: rgb(2, 171, 0);
                padding: 5px;
                border: 1px solid rgb(2, 171, 0);
                border-radius: 5px;
            }
        
            QPushButton#bnt_creat_subjet::hover{
                background-color: rgb(2, 171, 0);
                color: white;
            }
        """)
        
        self.stackedWidget.addWidget(self.page_creat_discuss)
        
        self.page_discuss = QtWidgets.QWidget()
        self.page_discuss.setObjectName("page_discuss")
        self.contenai_discuss = QtWidgets.QScrollArea(self.page_discuss)
        self.contenai_discuss.setGeometry(QtCore.QRect(0, 0, 755, 671))
        self.contenai_discuss.setStyleSheet("""
            QScrollArea#contenai_discuss {
                border: 0px;
            }
            
            QWidget#discuss{
                background-color: rgb(255, 255, 255);
            "}
        """)
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
        self.contenai_subjet.setStyleSheet("""
            QScrollArea#contenai_subjet {
                border: 0px;
                }

            QWidget#subjet{
                background-color: rgb(255, 255, 255);
            }
        """)
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
        self.frame_connection.setStyleSheet("""
            QFrame#frame_connection{
                background-color: rgb(255, 255, 255);
            }
        """)
        self.frame_connection.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_connection.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_connection.setObjectName("frame_connection")
        self.enter_email_connection = QtWidgets.QLineEdit(self.frame_connection)
        self.enter_email_connection.setGeometry(QtCore.QRect(230, 289, 331, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.enter_email_connection.setFont(font)
        self.enter_email_connection.setStyleSheet("""
            QLineEdit#enter_email_connection{
                background-color: rgb(236, 236, 236);
                padding: 5px;
                border: 1px solid rgb(160, 161, 182);
                border-left: 0px;
                border-right: 0px;
                border-top: 0px;
            }

            QLineEdit#enter_email_connection::hover {
                border-bottom-color:  rgb(64, 40, 200);
            }
        """)
        self.enter_email_connection.setObjectName("enter_email_connection")
        self.label_connection_2 = QtWidgets.QLabel(self.frame_connection)
        self.label_connection_2.setGeometry(QtCore.QRect(320, 210, 181, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label_connection_2.setFont(font)
        self.label_connection_2.setObjectName("label_connection_2")
        self.enter_password_connection = QtWidgets.QLineEdit(self.frame_connection)
        self.enter_password_connection.setGeometry(QtCore.QRect(230, 340, 331, 31))
        self.enter_password_connection.setEchoMode(QtWidgets.QLineEdit.Password)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.enter_password_connection.setFont(font)
        self.enter_password_connection.setStyleSheet("""QLineEdit#enter_password_connection{
"background-color: rgb(236, 236, 236);
"padding: 5px;
"border: 1px solid rgb(160, 161, 182);
"border-left: 0px;
"border-right: 0px;
"border-top: 0px;
"}
"
"QLineEdit#enter_password_connection::hover {
"border-bottom-color: rgb(64, 40, 200);
"
"}""")
        self.enter_password_connection.setObjectName("enter_password_connection")
        self.bnt_connection = QtWidgets.QPushButton(self.frame_connection)
        self.bnt_connection.clicked.connect(self.connection_user)
        self.bnt_connection.setGeometry(QtCore.QRect(280, 400, 211, 31))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(14)
        self.bnt_connection.setFont(font)
        self.bnt_connection.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bnt_connection.setStyleSheet("""
            QPushButton#bnt_connection{
            background-color: white;
            color: rgb(64, 40, 200);
            padding: 5px;
            border: 2px solid rgb(64, 40, 200);
            border-radius: 5px;
            }

            QPushButton#bnt_connection::hover{
            background-color: rgb(64, 40, 200);
            color: white;
            }
        """)
        self.bnt_connection.setObjectName("bnt_connection")
        self.lien_subscription = QtWidgets.QPushButton(self.frame_connection)
        self.lien_subscription.clicked.connect(self.window_subscription)
        self.lien_subscription.setGeometry(QtCore.QRect(420, 450, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.lien_subscription.setFont(font)
        self.lien_subscription.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.lien_subscription.setStyleSheet("""
            QPushButton#lien_subscription{
                background-color: rgb(255, 255, 255);
                color:  rgb(64, 40, 200);
                border: 0px;
            }

            QPushButton#lien_subscription::hover{
                font-weight: bold;
            }
        """)
        self.lien_subscription.setObjectName("lien_subscription")
        self.label_unitile = QtWidgets.QLabel(self.frame_connection)
        self.label_unitile.setGeometry(QtCore.QRect(235, 458, 201, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.label_unitile.setFont(font)
        self.label_unitile.setObjectName("label_unitile")
        self.stackedWidget.addWidget(self.page_connection)
        self.page_subscription = QtWidgets.QWidget()
        self.page_subscription.setObjectName("page_subscription")
        self.frame_subscribtion = QtWidgets.QFrame(self.page_subscription)
        self.frame_subscribtion.setGeometry(QtCore.QRect(0, 0, 714, 672))
        self.frame_subscribtion.setStyleSheet("QFrame#frame_subscribtion{ background-color: rgb(255, 255, 255);}")
        self.frame_subscribtion.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_subscribtion.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_subscribtion.setObjectName("frame_subscribtion")
        self.enter_email = QtWidgets.QLineEdit(self.frame_subscribtion)
        self.enter_email.setGeometry(QtCore.QRect(226, 269, 331, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.enter_email.setFont(font)
        self.enter_email.setStyleSheet("""
            QLineEdit#enter_email{
                background-color: rgb(236, 236, 236);
                border-radius: 3px;
                padding: 5px;
                border: 1px solid rgb(160, 161, 182);
                border-left: 0px;
                border-right: 0px;
                border-top: 0px;
            }

            QLineEdit#enter_email::hover {
                border-bottom-color:  rgb(64, 40, 200);

            }
        """)
        self.enter_email.setObjectName("enter_email")
        self.bnt_subcription = QtWidgets.QPushButton(self.frame_subscribtion)
        self.bnt_subcription.clicked.connect(self.recording_user)
        self.bnt_subcription.setGeometry(QtCore.QRect(286, 514, 211, 31))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(14)
        self.bnt_subcription.setFont(font)
        self.bnt_subcription.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bnt_subcription.setStyleSheet("""
            QPushButton#bnt_subcription{
                background-color: white;
                color: rgb(64, 40, 200);
                padding: 5px;
                border: 2px solid rgb(64, 40, 200);
                border-radius: 5px;
            }


            QPushButton#bnt_subcription::hover{
                background-color: rgb(64, 40, 200);
                color: white;
            }
        """)
        self.bnt_subcription.setObjectName("bnt_subcription")
        self.enter_last_name = QtWidgets.QLineEdit(self.frame_subscribtion)
        self.enter_last_name.setGeometry(QtCore.QRect(226, 164, 331, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.enter_last_name.setFont(font)
        self.enter_last_name.setStyleSheet("""
            QLineEdit#enter_last_name{
                background-color: rgb(236, 236, 236);
                border-radius: 3px;
                padding: 5px;
                border: 1px solid rgb(160, 161, 182);
                border-left: 0px;
                border-right: 0px;
                border-top: 0px;
            }

            QLineEdit#enter_last_name::hover {
                border-bottom-color: rgb(64, 40, 200);
            }
        """)
        self.enter_last_name.setObjectName("enter_last_name")
        self.enter_first_name = QtWidgets.QLineEdit(self.frame_subscribtion)
        self.enter_first_name.setGeometry(QtCore.QRect(226, 218, 331, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.enter_first_name.setFont(font)
        self.enter_first_name.setStyleSheet("""
            QLineEdit#enter_first_name{
                background-color: rgb(236, 236, 236);
                border-radius: 3px;
                padding: 5px;
                border: 1px solid rgb(160, 161, 182);
                border-left: 0px;
                border-right: 0px;
                border-top: 0px;
            }

            QLineEdit#enter_first_name::hover {
                border-bottom-color:  rgb(64, 40, 200);
            }
            """)
        self.enter_first_name.setObjectName("enter_first_name")
        self.enter_password_2 = QtWidgets.QLineEdit(self.frame_subscribtion)
        self.enter_password_2.setGeometry(QtCore.QRect(226, 457, 331, 31))
        self.enter_password_2.setEchoMode(QtWidgets.QLineEdit.Password)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.enter_password_2.setFont(font)
        self.enter_password_2.setStyleSheet("""
            QLineEdit#enter_password_2{
                background-color: rgb(236, 236, 236);
                border-radius: 3px;
                padding: 5px;
                border: 1px solid rgb(160, 161, 182);
                border-left: 0px;
                border-right: 0px;
                border-top: 0px;
            }
                
            QLineEdit#enter_password_2::hover {
                border-bottom-color:  rgb(64, 40, 200);
            }
        """)
        self.enter_password_2.setObjectName("enter_password_2")
        self.enter_password_1 = QtWidgets.QLineEdit(self.frame_subscribtion)
        self.enter_password_1.setGeometry(QtCore.QRect(226, 410, 331, 31))
        self.enter_password_1.setEchoMode(QtWidgets.QLineEdit.Password)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.enter_password_1.setFont(font)
        self.enter_password_1.setStyleSheet("""
            QLineEdit#enter_password_1{
                background-color: rgb(236, 236, 236);
                border-radius: 3px;
                padding: 5px;
                border: 1px solid rgb(160, 161, 182);
                border-left: 0px;
                border-right: 0px;
                border-top: 0px;
            }

            QLineEdit#enter_password_1::hover {
                border-bottom-color:  rgb(64, 40, 200);
            }
        """)
        self.enter_password_1.setObjectName("enter_password_1")
        self.enter_gender = QtWidgets.QComboBox(self.frame_subscribtion)
        self.enter_gender.addItem("Homme")
        self.enter_gender.addItem("Femme")
        self.enter_gender.setGeometry(QtCore.QRect(226, 324, 331, 24))
        self.enter_gender.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.enter_gender.setStyleSheet("""
            QComboBox#enter_gender {
                border-left: 0px; 
                border-top: 0px; 
                border-right: 0px;
                border-radius: 3px; 
                border-bottom: 1px solid rgb(204, 204, 204); 
                background-color: rgb(236, 236, 236);
                color: black;
            }
            
            QComboBox#enter_gender::hover {
                border-bottom-color: rgb(160, 161, 182);
            }
        """)
        self.enter_gender.setObjectName("enter_gender")
        self.enter_class = QtWidgets.QComboBox(self.frame_subscribtion)
        list_class = ["6éme", "5éme", "4éme", "3éme", "2nd", "1ère", "Terminal"]
        for item in list_class: self.enter_class.addItem(item)
        self.enter_class.setGeometry(QtCore.QRect(226, 366, 331, 24))
        self.enter_class.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.enter_class.setStyleSheet("""
            QComboBox#enter_class {
                border-left: 0px; 
                border-top: 0px; 
                border-radius: 3px;
                border-right: 0px;
                border-bottom: 1px solid rgb(204, 204, 204); 
                background-color: rgb(236, 236, 236);
                color: black;
            }

            QComboBox#enter_classr::hover {
                border-bottom-color: rgb(160, 161, 182);
            }
        """)
        self.enter_class.setObjectName("enter_class")
        self.label_subscription = QtWidgets.QLabel(self.frame_subscribtion)
        self.label_subscription.setGeometry(QtCore.QRect(315, 84, 171, 61))
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
        self.lien_connection.setGeometry(QtCore.QRect(410, 562, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.lien_connection.setFont(font)
        self.lien_connection.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.lien_connection.setStyleSheet("""
            QPushButton#lien_connection{
                background-color: rgb(255, 255, 255);
                color:  rgb(64, 40, 200);
                border: 0px;
            }

            QPushButton#lien_connection::hover{
                font-weight: bold;
            }"""
        )
        self.lien_connection.setObjectName("lien_connection")
        self.label_unitile_2 = QtWidgets.QLabel(self.frame_subscribtion)
        self.label_unitile_2.setGeometry(QtCore.QRect(229, 570, 201, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.label_unitile_2.setFont(font)
        self.label_unitile_2.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.label_unitile_2.setStyleSheet("")
        self.label_unitile_2.setObjectName("label_unitile_2")
        self.stackedWidget.addWidget(self.page_subscription)
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(0, 0, 311, 671))
        self.scrollArea.setStyleSheet("QScrollArea#scrollArea{ border: 0px;}")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.bar_nav = QtWidgets.QWidget()
        self.bar_nav.setGeometry(QtCore.QRect(0, 0, 311, 671))
        self.bar_nav.setObjectName("bar_nav")
        self.frame_conne_1 = Frame(self.bar_nav)
        self.frame_conne_1.clicked.connect(self.window_connection)
        self.frame_conne_1.setGeometry(QtCore.QRect(10, 572, 311, 80))
        self.frame_conne_1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.frame_conne_1.setStyleSheet("""
            QFrame#frame_conne_1::hover{
                background-color: rgb(204, 204, 204);
            }
            
            QFrame#frame_conne_1{
                border: 0px;
            }
        """)
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
        self.frame_category_4.setStyleSheet("""
            QFrame#frame_category_4::hover{
                background-color: rgb(204, 204, 204);
            }
            
            QFrame#frame_category_4{
                border: 0px;
            }
            """)
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
        self.logo_6.setPixmap(QtGui.QPixmap(os.path.join(folder_img, "question.png")))
        self.logo_6.setScaledContents(True)
        self.logo_6.setObjectName("logo_6")
        
        # Frame ajout un sujet
        self.frame_reply = Frame(self.bar_nav)
        self.frame_reply.clicked.connect(self.window_creat_subjet)
        self.frame_reply.setGeometry(QtCore.QRect(10, 450, 311, 80))
        self.frame_reply.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.frame_reply.setStyleSheet("""
            QFrame#frame_reply::hover{
                background-color: rgb(204, 204, 204);
            }
            
            QFrame#frame_reply{
                border: 0px;
            }
            """)
        self.frame_reply.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_reply.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_reply.setObjectName("frame_reply")
        self.label_subjet = QtWidgets.QLabel(self.frame_reply)
        self.label_subjet.setGeometry(QtCore.QRect(110, 31, 150, 32))
        self.label_subjet.setText("Créé un sujet")
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(16)
        self.label_subjet.setFont(font)
        self.label_subjet.setObjectName("label_subjet")
        self.label_img_subjet = QtWidgets.QLabel(self.frame_reply)
        self.label_img_subjet.setGeometry(QtCore.QRect(16, 10, 71, 70))
        self.label_img_subjet.setPixmap(QtGui.QPixmap(os.path.join(folder_img, "people.png")))
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
        self.frame_category_2.setGeometry(QtCore.QRect(5, 171, 311, 61))
        self.frame_category_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.frame_category_2.setStyleSheet("""
            QFrame#frame_category_2::hover{
                background-color: rgb(204, 204, 204);
            }
            
            QFrame#frame_category_2{
                border: 0px;
            }
            """)
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
        self.logo_2.setGeometry(QtCore.QRect(30, 2, 61, 51))
        self.logo_2.setPixmap(QtGui.QPixmap(os.path.join(folder_img, "new_chimie.png")))
        self.logo_2.setScaledContents(True)
        self.logo_2.setObjectName("logo_2")
        self.frame_category_3 = Frame(self.bar_nav)
        self.frame_category_3.clicked.connect(partial(self.window_subjets, "svt"))
        self.frame_category_3.setGeometry(QtCore.QRect(5, 102, 311, 61))
        self.frame_category_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.frame_category_3.setStyleSheet("""
            QFrame#frame_category_3::hover{
                background-color: rgb(204, 204, 204);
            }
            
            QFrame#frame_category_3{
                border: 0px;
            }
            """)
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
        self.logo.setPixmap(QtGui.QPixmap(os.path.join(folder_img, "planete-terre")))
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
        self.frame_category_6.setStyleSheet("""
            QFrame#frame_category_6::hover{
                background-color: rgb(204, 204, 204);
            }
            
            QFrame#frame_category_6{
                border: 0px;
            }
            """)
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
        self.logo_4.setGeometry(QtCore.QRect(30, 10, 61, 51))
        self.logo_4.setPixmap(QtGui.QPixmap(os.path.join(folder_img, "eng.png")))
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
        self.label_unitile.setText(_translate("MainWindow", "Vous n'avez pas de compte ?"))
        self.enter_email.setPlaceholderText(_translate("MainWindow", "Addresse email"))
        self.bnt_subcription.setText(_translate("MainWindow", "Inscription"))
        self.enter_last_name.setPlaceholderText(_translate("MainWindow", "Nom"))
        self.enter_first_name.setPlaceholderText(_translate("MainWindow", "Prénom"))
        self.enter_password_2.setPlaceholderText(_translate("MainWindow", "Comfirmer le mot de passe"))
        self.enter_password_1.setPlaceholderText(_translate("MainWindow", "Mot de passe"))
        self.enter_title_subjet.setPlaceholderText(_translate("MainWindow", "Entrer le titre du subjet"))
        self.label_subscription.setText(_translate("MainWindow", "Inscription"))
        self.lien_connection.setText(_translate("MainWindow", "Connecter vous ici"))
        self.label_unitile_2.setText(_translate("MainWindow", "Vous avez déja un compte ?"))
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
