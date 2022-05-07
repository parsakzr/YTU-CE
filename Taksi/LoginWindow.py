from operator import index
from PyQt5 import QtCore, QtGui, QtWidgets
from ManagerWindow import *
from CustomerLogin import *
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

import backend.auth as auth


class Ui_LoginWindow(object):
    

    
    def openWindow(self):    ## OPENING SECOND WINDOW and should check user id and password
        index = self.typeofUserComboBox.currentText()

        if index == "Müdür":
            self.window = QtWidgets.QMainWindow()
            self.ui = Ui_ManagerWindow()
            self.ui.setupUi(self.window)
            self.window.show()
        if index == "Müşteri":
            self.window = QtWidgets.QMainWindow()
            self.ui = Ui_CustomerLoginWindow()
            self.ui.setupUi(self.window)
            self.window.show()

    def registerUser(self): ## SAVING USER TO DATABASE
        index = self.typeofUserComboBox.currentText()
        if index == "Müdür": # tranlate to manager
            index = "manager"
        else:
            index = "customer"
        
        username = self.useridInput.text()
        password = self.passwordInput.text()

        isOk = auth.addUser(username, password, index)
        if isOk:
            self.openWindow()
        else:
            self.useridInput.setText("Daha once kullaniliyor")

    def loginUser(self): ## CHECKING USER ID AND PASSWORD
        index = self.typeofUserComboBox.currentText()
        if index == "Müdür": # tranlate to manager
            index = "manager"
        else:
            index = "customer"
        
        username = self.useridInput.text()
        password = self.passwordInput.text()

        isOk = auth.login(username, password)
        if isOk:
            self.openWindow()
        else:
            self.useridInput.setText("Kullanıcı adı veya şifre yanlış")


    def setupUi(self, LoginWindow):
        LoginWindow.setObjectName("LoginWindow")
        LoginWindow.resize(306, 353)
        self.centralwidget = QtWidgets.QWidget(LoginWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, -1, -1, 0)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.logintitleText = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logintitleText.sizePolicy().hasHeightForWidth())
        self.logintitleText.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.logintitleText.setFont(font)
        self.logintitleText.setObjectName("logintitleText")
        self.verticalLayout.addWidget(self.logintitleText)
        self.typeofUserComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.typeofUserComboBox.setObjectName("typeofUserComboBox")
        self.typeofUserComboBox.addItem("")
        self.typeofUserComboBox.addItem("")
        self.typeofUserComboBox.addItem("")
        self.verticalLayout.addWidget(self.typeofUserComboBox)
        self.useridLabel = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.useridLabel.sizePolicy().hasHeightForWidth())
        self.useridLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.useridLabel.setFont(font)
        self.useridLabel.setObjectName("useridLabel")
        self.verticalLayout.addWidget(self.useridLabel)
        self.useridInput = QtWidgets.QLineEdit(self.centralwidget)
        self.useridInput.setObjectName("useridInput")
        self.verticalLayout.addWidget(self.useridInput)
        self.passwordLabel = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.passwordLabel.sizePolicy().hasHeightForWidth())
        self.passwordLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.passwordLabel.setFont(font)
        self.passwordLabel.setObjectName("passwordLabel")
        self.verticalLayout.addWidget(self.passwordLabel)
        self.passwordInput = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.passwordInput.sizePolicy().hasHeightForWidth())
        self.passwordInput.setSizePolicy(sizePolicy)
        self.passwordInput.setObjectName("passwordInput")
        self.verticalLayout.addWidget(self.passwordInput)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        ## OPENING MANAGER WINDOW
        self.loginButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.loginUser())  ## OPENING MGR WINDOW IF PUSHED
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loginButton.sizePolicy().hasHeightForWidth())
        self.loginButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.loginButton.setFont(font)
        self.loginButton.setObjectName("loginButton")
        self.gridLayout.addWidget(self.loginButton, 1, 0, 1, 1)
        self.registerButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda : self.registerUser()) # WILL CONNECT VIA  "... , clicked = lambda: self.funcName())" # TODO
        # self.registerButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda : self.openWindow()) # WILL CONNECT VIA  "... , clicked = lambda: self.funcName())" # TODO
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.registerButton.sizePolicy().hasHeightForWidth())
        self.registerButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.registerButton.setFont(font)
        self.registerButton.setObjectName("registerButton")
        self.gridLayout.addWidget(self.registerButton, 2, 0, 1, 1)
        LoginWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(LoginWindow)
        self.statusbar.setObjectName("statusbar")
        LoginWindow.setStatusBar(self.statusbar)

        self.retranslateUi(LoginWindow)
        QtCore.QMetaObject.connectSlotsByName(LoginWindow)

    def retranslateUi(self, LoginWindow):
        _translate = QtCore.QCoreApplication.translate
        LoginWindow.setWindowTitle(_translate("LoginWindow", "MainWindow"))
        self.logintitleText.setText(_translate("LoginWindow", "Taksi Durağı Sistemi"))
        self.typeofUserComboBox.setItemText(0, _translate("LoginWindow", "Seçiniz (Müşteri/Müdür)"))
        self.typeofUserComboBox.setItemText(1, _translate("LoginWindow", "Müşteri"))
        self.typeofUserComboBox.setItemText(2, _translate("LoginWindow", "Müdür"))
        self.useridLabel.setText(_translate("LoginWindow", "Kullanıcı ID"))
        self.passwordLabel.setText(_translate("LoginWindow", "Şifre"))
        self.loginButton.setText(_translate("LoginWindow", "Giriş Yap"))
        self.registerButton.setText(_translate("LoginWindow", "Kayıt Ol"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    LoginWindow = QtWidgets.QMainWindow()
    ui = Ui_LoginWindow()
    ui.setupUi(LoginWindow)
    LoginWindow.show()
    sys.exit(app.exec_())


