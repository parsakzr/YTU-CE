from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from CustomerReview import *

class Ui_CustomerLoginWindow(object):
    headersRegion = [" ","Bakırköy", "Beşiktaş", "Esenler", "Kadıköy", "Maltepe", "Sarıyer", "Üsküdar"]
    headersCarStatus_C = ["Plaka", "Tip", "Model", "Yıl", "Motor Gücü", "Bölge", "Taban Fiyatı", "Uygunluk"]

    def callTaxi(self): #OPENS REVIEW WINDOW IF CUSTOMER CALLS A TAXI
        input = self.plateNr.text()  # Plate Number of the selected taxi
        address = self.addressInput.toPlainText() # to save the addres data
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_CustomerReviewWindow()
        self.ui.setupUi(self.window)
        self.window.show()


    def searchTaxi(self):
        input = self.closestStationComboBox.currentText() # TO LIST AVAILABLE TAXIS FROM SELECTED STATION

        # rows = len(self.data)             ## SOMETHING LIKE THAT TO PRINT TABLE TODO
        # columns = len(self.data[0])
        # for i in range(rows):
        #     for j in range(columns):
        #         print(self.data[i][j])
        #         self.viewcarstatusTable.setItem(i, j, QtWidgets.QTableWidgetItem(self.data[i][j]))



    def setupUi(self, musteriGiris):
        musteriGiris.setObjectName("musteriGiris")
        musteriGiris.resize(455, 481)
        self.centralwidget = QtWidgets.QWidget(musteriGiris)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setContentsMargins(6, 6, 6, 6)
        self.formLayout.setObjectName("formLayout")
        self.closestStationLabel = QtWidgets.QLabel(self.centralwidget)
        self.closestStationLabel.setObjectName("closestStationLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.closestStationLabel)
        self.closestStationComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.closestStationComboBox.setObjectName("closestStationComboBox")
        self.closestStationComboBox.setItemText(0, "")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.closestStationComboBox)
        self.addressLabel = QtWidgets.QLabel(self.centralwidget)
        self.addressLabel.setObjectName("addressLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.addressLabel)
        self.searchTaxiButton = QtWidgets.QPushButton(self.centralwidget,clicked = lambda :self.searchTaxi()) ## WILL CONNECT SEARCH QUERY VIA  "... , clicked = lambda: self.funcName())" # TODO
        self.searchTaxiButton.setObjectName("searchTaxiButton")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.searchTaxiButton)
        self.addressInput = QtWidgets.QTextEdit(self.centralwidget)
        self.addressInput.setObjectName("addressInput")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.addressInput)
        self.gridLayout_2.addLayout(self.formLayout, 0, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(7, 6, 6, 6)
        self.gridLayout.setObjectName("gridLayout")
        self.availableCarsTable_c = QtWidgets.QTableWidget(self.centralwidget)
        self.availableCarsTable_c.setObjectName("availableCarsTable_c")


        self.availableCarsTable_c.setColumnCount(len(self.headersCarStatus_C))

        for i in range(len(self.headersCarStatus_C)):
            item = QtWidgets.QTableWidgetItem(self.headersCarStatus_C[i])
            self.availableCarsTable_c.setHorizontalHeaderItem(i, item)

        self.availableCarsTable_c.setRowCount(0) # LENGTH


        self.gridLayout.addWidget(self.availableCarsTable_c, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.driveridLabel_Customer = QtWidgets.QLabel(self.centralwidget)
        self.driveridLabel_Customer.setObjectName("driveridLabel_Customer")
        self.verticalLayout.addWidget(self.driveridLabel_Customer)
        self.plateNr = QtWidgets.QLineEdit(self.centralwidget)
        self.plateNr.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.plateNr)

        self.callTaxiButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.callTaxi()) ## WILL CONNECT CALL TAXI FUNCTION VIA  "... , clicked = lambda: self.funcName())" #TODO

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.callTaxiButton.sizePolicy().hasHeightForWidth())


        self.callTaxiButton.setSizePolicy(sizePolicy)
        self.callTaxiButton.setObjectName("callTaxiButton")

        self.verticalLayout.addWidget(self.callTaxiButton)
        self.gridLayout_2.addLayout(self.verticalLayout, 2, 0, 1, 1)
        musteriGiris.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(musteriGiris)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 455, 21))
        self.menubar.setObjectName("menubar")
        musteriGiris.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(musteriGiris)
        self.statusbar.setObjectName("statusbar")
        musteriGiris.setStatusBar(self.statusbar)

        self.retranslateUi(musteriGiris)
        QtCore.QMetaObject.connectSlotsByName(musteriGiris)

    def retranslateUi(self, musteriGiris):
        _translate = QtCore.QCoreApplication.translate
        musteriGiris.setWindowTitle(_translate("musteriGiris", "MainWindow"))
        self.closestStationLabel.setText(_translate("musteriGiris", "En Yakın Durak"))

        for i in range(len(self.headersRegion)):
            self.closestStationComboBox.addItem("")
            self.closestStationComboBox.setItemText(i, _translate("MainWindow", self.headersRegion[i]))

        self.addressLabel.setText(_translate("musteriGiris", "Detaylı Adres"))
        self.searchTaxiButton.setText(_translate("musteriGiris", "Taksi Ara"))
        self.driveridLabel_Customer.setText(_translate("musteriGiris", "Plaka Giriniz:"))
        self.callTaxiButton.setText(_translate("musteriGiris", "Taksi Çağır"))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    musteriGirisUI = QtWidgets.QMainWindow()
    ui = Ui_CustomerLoginWindow()
    ui.setupUi(musteriGirisUI)
    musteriGirisUI.show()
    sys.exit(app.exec_())