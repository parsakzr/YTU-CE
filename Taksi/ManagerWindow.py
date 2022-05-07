from decimal import Decimal
from dis import dis
from PyQt5 import QtCore, QtGui, QtWidgets

import backend.car as Car
import backend.driver as Driver
import backend.trip as Trip

class Ui_ManagerWindow(object):
    data = []
    headersCarStatus = ["Plaka", "Tip", "Model", "Yıl", "Motor Gücü", "Bölge", "Taban Fiyatı", "Uygunluk"]
    headersRegion = ["","Bakırköy", "Beşiktaş", "Esenler", "Kadıköy", "Maltepe", "Sarıyer", "Üsküdar"]
    headersDriverTable = ["ID", "İsim", "Soyisim", "Plaka", "Durak", "Puan", "Adres"]
    headersCar = ["Plaka", "Tip", "Model", "Yıl", "Motor", "Bölge", "Taban Fiyatı", "Uygunluğu"]
    headersTripTable = ["Trip ID", "Sürücü ID", "Araç ID", "Başlangıç Konumu", "Bitiş Konumu", "Başlangıç Zamanı","Bitiş Zamanı", "Fiyat", "Puan"]
    headersCarType = ["","Coupe","Sedan","SUV"]


    def displayData(self, table): # show data in table
        if (self.data == None or self.data == []):
            return
        
        table.setRowCount(len(self.data)) ## LENGTH OF THE OUTPUT DATA
        print(self.data) #LOG
        rows = len(self.data)
        columns = len(self.data[0])
        for i in range(rows):
            for j in range(columns):
                # print(self.data[i][j])
                table.setItem(i, j, QtWidgets.QTableWidgetItem(str(self.data[i][j])))


    def refreshTrips(self):
        print("hehe")
        ##insert query

    def filterDrivers(self):
        driverID = self.driveridInput.text()
        driverName = self.drivernameInput.text()
        driverSurname = self.driversurnameInput.text()
        region = self.regionComboBox.currentText()

        ## should print the table TODO


    def filterCars(self):
        plate = self.plateInput.text()
        model = self.carmodelTextInput.text()
        type = self.cartypeComboBox.currentText()
        region = self.carregionComboBox.currentText()

        if(plate + model + type + region == ""): # no filter applied
            self.data = Car.getAllCars()
            print("Get All Cars", self.data)

        elif (plate != ""):
            self.data = Car.getCar(plate)
            print("Get Car", self.data)
        else:
            self.data = Car.getCars_filtered(car_model=model, car_type=type, car_loc=region)
            print("Get Cars by Filter", self.data)
        
        self.displayData(self.carTable)


    def showAvailableCars(self):
        self.data = Car.getAvailableCars()
        self.displayData(self.viewcarstatusTable)
        

    def showOccupiedCars(self):
        self.data = Car.getOccupiedCars()
        self.displayData(self.viewcarstatusTable)


    def setupUi(self, MudurEkrani):
        MudurEkrani.setObjectName("MudurEkrani")
        MudurEkrani.resize(722, 588)
        self.centralwidget = QtWidgets.QWidget(MudurEkrani)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab1 = QtWidgets.QWidget()
        self.tab1.setObjectName("tab1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(0, 28, -1, 28)
        self.horizontalLayout_4.setSpacing(13)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.viewavailableCarsButton = QtWidgets.QPushButton(self.tab1, clicked = lambda: self.showAvailableCars())
        self.viewavailableCarsButton.setObjectName("viewavailableCarsButton")
        self.horizontalLayout_4.addWidget(self.viewavailableCarsButton)

        ## CAR AVAILABILITY ##
        self.viewoccupiedCarsButton = QtWidgets.QPushButton(self.tab1) ## TODO
        self.viewoccupiedCarsButton.setObjectName("viewoccupiedCarsButton")


        self.horizontalLayout_4.addWidget(self.viewoccupiedCarsButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_5.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")

        ## CAR STATUS TABLE ##
        self.viewcarstatusTable = QtWidgets.QTableWidget(self.tab1)
        self.viewcarstatusTable.setObjectName("viewcarstatusTable")
        self.viewcarstatusTable.setColumnCount(len(self.headersCarStatus))
        self.viewcarstatusTable.setRowCount(len(self.data)) ## LENGTH OF THE OUTPUT DATA

        for i in range(len(self.headersCarStatus)):
            item = QtWidgets.QTableWidgetItem()
            self.viewcarstatusTable.setHorizontalHeaderItem(i, item)


        self.horizontalLayout_5.addWidget(self.viewcarstatusTable)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.tabWidget.addTab(self.tab1, "")


        ## DRIVER TAB ##
        self.tab2 = QtWidgets.QWidget()
        self.tab2.setObjectName("tab2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tab2_1 = QtWidgets.QTabWidget(self.tab2)
        self.tab2_1.setObjectName("tab2_1")
        self.driverTab = QtWidgets.QWidget()
        self.driverTab.setObjectName("driverTab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.driverTab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout_7 = QtWidgets.QFormLayout()
        self.formLayout_7.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.formLayout_7.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_7.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout_7.setFormAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.formLayout_7.setContentsMargins(6, 6, 6, 0)
        self.formLayout_7.setHorizontalSpacing(4)
        self.formLayout_7.setVerticalSpacing(6)
        self.formLayout_7.setObjectName("formLayout_7")
        self.drivernameLabel = QtWidgets.QLabel(self.driverTab)
        self.drivernameLabel.setObjectName("drivernameLabel")
        self.formLayout_7.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.drivernameLabel)
        self.drivernameInput = QtWidgets.QLineEdit(self.driverTab)
        self.drivernameInput.setObjectName("drivernameInput")
        self.formLayout_7.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.drivernameInput)
        self.driversurnameLabel = QtWidgets.QLabel(self.driverTab)
        self.driversurnameLabel.setObjectName("driversurnameLabel")
        self.formLayout_7.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.driversurnameLabel)
        self.driversurnameInput = QtWidgets.QLineEdit(self.driverTab)
        self.driversurnameInput.setObjectName("driversurnameInput")
        self.formLayout_7.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.driversurnameInput)
        self.driverregionLabel = QtWidgets.QLabel(self.driverTab)
        self.driverregionLabel.setObjectName("driverregionLabel")
        self.formLayout_7.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.driverregionLabel)
        self.regionComboBox = QtWidgets.QComboBox(self.driverTab)
        self.regionComboBox.setObjectName("regionComboBox")
        self.regionComboBox.setItemText(0, "")
        self.formLayout_7.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.regionComboBox)
        self.filterDriversButton = QtWidgets.QPushButton(self.driverTab, clicked = lambda : self.filterDrivers())  # WILL CONNECT TO FILTER DRIVER FUNCTION VIA  "... , clicked = lambda: self.funcName())" #TODO
        self.filterDriversButton.setObjectName("filterDriversButton")
        self.formLayout_7.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.filterDriversButton)
        self.driveridLabel = QtWidgets.QLabel(self.driverTab)
        self.driveridLabel.setObjectName("driveridLabel")
        self.formLayout_7.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.driveridLabel)
        self.driveridInput = QtWidgets.QLineEdit(self.driverTab)
        self.driveridInput.setObjectName("driveridInput")
        self.formLayout_7.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.driveridInput)
        self.verticalLayout.addLayout(self.formLayout_7)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_6.setContentsMargins(6, 6, 6, 6)
        self.horizontalLayout_6.setSpacing(4)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")

        ## DRIVER TABLE
        self.driverTable = QtWidgets.QTableWidget(self.driverTab)
        self.driverTable.setObjectName("driverTable")

        self.driverTable.setColumnCount(len(self.headersDriverTable))
        self.driverTable.setRowCount(0) ## length

        for i in range(len(self.headersDriverTable)):
            item = QtWidgets.QTableWidgetItem()
            self.driverTable.setHorizontalHeaderItem(i, item)


        self.horizontalLayout_6.addWidget(self.driverTable)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.tab2_1.addTab(self.driverTab, "")

        ## CAR TAB
        self.carTab = QtWidgets.QWidget()
        self.carTab.setObjectName("carTab")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.carTab)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.formLayout_4 = QtWidgets.QFormLayout()
        self.formLayout_4.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.formLayout_4.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_4.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout_4.setFormAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.formLayout_4.setContentsMargins(6, 6, 6, 0)
        self.formLayout_4.setHorizontalSpacing(4)
        self.formLayout_4.setVerticalSpacing(6)
        self.formLayout_4.setObjectName("formLayout_4")
        self.plateLabel = QtWidgets.QLabel(self.carTab)
        self.plateLabel.setObjectName("plateLabel")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.plateLabel)
        self.plateInput = QtWidgets.QLineEdit(self.carTab)
        self.plateInput.setObjectName("plateInput")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.plateInput)
        self.carmodelLabel = QtWidgets.QLabel(self.carTab)
        self.carmodelLabel.setObjectName("carmodelLabel")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.carmodelLabel)
        self.carmodelTextInput = QtWidgets.QLineEdit(self.carTab)
        self.carmodelTextInput.setObjectName("carmodelTextInput")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.carmodelTextInput)
        self.carregionLabel = QtWidgets.QLabel(self.carTab)
        self.carregionLabel.setObjectName("carregionLabel")
        self.formLayout_4.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.carregionLabel)
        self.carregionComboBox = QtWidgets.QComboBox(self.carTab)
        self.carregionComboBox.setObjectName("carregionComboBox")
        self.carregionComboBox.setItemText(0, "")
        self.formLayout_4.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.carregionComboBox)
        self.carFilterButton = QtWidgets.QPushButton(self.carTab, clicked = lambda : self.filterCars()) ## WILL CONNECT TO FILTER VIA  "... , clicked = lambda: self.funcName())" # TODO
        self.carFilterButton.setObjectName("carFilterButton")
        self.formLayout_4.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.carFilterButton)
        self.cartypeLabel = QtWidgets.QLabel(self.carTab)
        self.cartypeLabel.setObjectName("cartypeLabel")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.cartypeLabel)
        self.cartypeComboBox = QtWidgets.QComboBox(self.carTab)
        self.cartypeComboBox.setObjectName("cartypeComboBox")
        self.cartypeComboBox.setItemText(0, "")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.cartypeComboBox)
        self.verticalLayout_6.addLayout(self.formLayout_4)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_9.setContentsMargins(6, 6, 6, 6)
        self.horizontalLayout_9.setSpacing(4)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")

        ## CAR TABLE ##
        self.carTable = QtWidgets.QTableWidget(self.carTab)
        self.carTable.setObjectName("carTable")
        self.carTable.setColumnCount(len(self.headersCar))
        self.carTable.setRowCount(0) ## LENGTH

        for i in range(len(self.headersCar)):
            item = QtWidgets.QTableWidgetItem()
            self.carTable.setHorizontalHeaderItem(i, item)

        ## TRIP TABLE ##
        self.horizontalLayout_9.addWidget(self.carTable)
        self.verticalLayout_6.addLayout(self.horizontalLayout_9)
        self.tab2_1.addTab(self.carTab, "")
        self.gridLayout_2.addWidget(self.tab2_1, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab2, "")
        self.tripsTab = QtWidgets.QWidget()
        self.tripsTab.setObjectName("tripsTab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tripsTab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tripTable = QtWidgets.QTableWidget(self.tripsTab)
        self.tripTable.setObjectName("tripTable")
        self.tripTable.setColumnCount(len(self.headersTripTable))

        self.tripTable.setRowCount(0) ## LENGTH


        for i in range(len(self.headersTripTable)):
            item = QtWidgets.QTableWidgetItem()
            self.tripTable.setHorizontalHeaderItem(i, item)

        ## REFRESH BUTTON ##
        self.verticalLayout_3.addWidget(self.tripTable)
        self.refreshtripButton = QtWidgets.QPushButton(self.tripsTab, clicked = lambda : self.refreshTrips()) ## WILL CONNECT VIA  "... , clicked = lambda: self.funcName())" # TODO
        self.refreshtripButton.setCheckable(False)
        self.refreshtripButton.setAutoDefault(False)
        self.refreshtripButton.setDefault(False)
        self.refreshtripButton.setFlat(False)
        self.refreshtripButton.setObjectName("refreshtripButton")
        self.verticalLayout_3.addWidget(self.refreshtripButton)
        self.tabWidget.addTab(self.tripsTab, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MudurEkrani.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MudurEkrani)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 722, 21))
        self.menubar.setObjectName("menubar")
        MudurEkrani.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MudurEkrani)
        self.statusbar.setObjectName("statusbar")
        MudurEkrani.setStatusBar(self.statusbar)

        self.retranslateUi(MudurEkrani)
        self.tabWidget.setCurrentIndex(0)
        self.tab2_1.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MudurEkrani)

    def retranslateUi(self, MudurEkrani):

        _translate = QtCore.QCoreApplication.translate
        MudurEkrani.setWindowTitle(_translate("MudurEkrani", "MainWindow"))
        self.viewavailableCarsButton.setText(_translate("MudurEkrani", "Boşta Olan Araçları Görüntüle"))
        self.viewoccupiedCarsButton.setText(_translate("MudurEkrani", "Dolu Olan Araçları Görüntüle"))


        for i in range(len(self.headersCarStatus)):
            item = self.viewcarstatusTable.horizontalHeaderItem(i)
            item.setText(_translate("MudurEkrani",self.headersCarStatus[i]))



        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab1), _translate("MudurEkrani", "Araç Durumları"))
        self.drivernameLabel.setText(_translate("MudurEkrani", "İsim"))
        self.driversurnameLabel.setText(_translate("MudurEkrani", "Soyisim"))
        self.driverregionLabel.setText(_translate("MudurEkrani", "Bölge"))



        for i in range(len(self.headersRegion)):
            self.regionComboBox.addItem("")
            self.regionComboBox.setItemText(i, _translate("MudurEkrani", self.headersRegion[i]))

        self.filterDriversButton.setText(_translate("MudurEkrani", "Filtrele"))
        self.driveridLabel.setText(_translate("MudurEkrani", "Sürücü ID"))



        for i in range(len(self.headersDriverTable)):
            item = self.driverTable.horizontalHeaderItem(i)
            item.setText(_translate("MudurEkrani",self.headersDriverTable[i]))

        self.tab2_1.setTabText(self.tab2_1.indexOf(self.driverTab), _translate("MudurEkrani", "Sürücü Bilgileri"))
        self.plateLabel.setText(_translate("MudurEkrani", "Plaka"))
        self.carmodelLabel.setText(_translate("MudurEkrani", "Model"))
        self.carregionLabel.setText(_translate("MudurEkrani", "Bölge"))

        for i in range(len(self.headersRegion)):
            self.carregionComboBox.addItem("")
            self.carregionComboBox.setItemText(i, _translate("MudurEkrani",self.headersRegion[i]))

        self.carFilterButton.setText(_translate("MudurEkrani", "Filtrele"))
        self.cartypeLabel.setText(_translate("MudurEkrani", "Tip"))

        for i in range(len(self.headersCarType)):
            self.cartypeComboBox.addItem("")
            self.cartypeComboBox.setItemText(i, _translate("MudurEkrani",self.headersCarType[i]))


        for i in range(len(self.headersCar)):
            item = self.carTable.horizontalHeaderItem(i)
            item.setText(_translate("MudurEkrani", self.headersCar[i]))


        self.tab2_1.setTabText(self.tab2_1.indexOf(self.carTab), _translate("MudurEkrani", "Araç Bilgileri"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab2), _translate("MudurEkrani", "Araç/Sürücü Bilgileri"))


        for i in range(len(self.headersTripTable)):
            item = self.tripTable.horizontalHeaderItem(i)
            item.setText(_translate("MudurEkrani", self.headersTripTable[i]))

        self.refreshtripButton.setText(_translate("MudurEkrani", "Yenile"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tripsTab), _translate("MudurEkrani", "Yolculuklar"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mgrWin = QtWidgets.QMainWindow()
    ui = Ui_ManagerWindow()
    ui.setupUi(mgrWin)
    mgrWin.show()
    sys.exit(app.exec_())