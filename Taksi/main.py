from ManagerWindow import *
from LoginWindow import *
from CustomerLogin import *
from CustomerReview import *
import sys

class LoginWindowUI(Ui_LoginWindow):
    
    def __init__(self,window):
        self.setupUi(window)
        self.data = []

        # self.viewavailableCarsButton.clicked.connect(self.showAvailableCars)
        # self.refreshtripButton.clicked.connect(self.refreshTrip)
        # self.viewoccupiedCarsButton.clicked.connect(self.showOccupiedCars)
        # self.carFilterButton.clicked.connect(self.filterCars)
        # self.filterDriversButton.clicked.connect(self.filterDrivers)

        # def refreshTrip(self):
        # def showOccupiedCars(self):
        # def filterDrivers(self):
        # def filterCars(self):

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Ui_LoginWindow = QtWidgets.QMainWindow()
    ui = LoginWindowUI(Ui_LoginWindow)
    Ui_LoginWindow.show()
    sys.exit(app.exec_())

