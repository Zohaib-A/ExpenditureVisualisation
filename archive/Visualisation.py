import sys
import pandas as py
from PyQt5.QtWidgets import *

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Application')
        self.setGeometry(100,100,800,800)

        #Label
        self.label = QLabel('Enter your Data Source URL: ', self)
        self.label.move(20,20)

        #Input Text Widget
        self.lineEdit = QLineEdit(self)
        self.lineEdit.move(300,10)
        self.lineEdit.resize(400, 50)

        #Create Button Widget
        self.button = QPushButton('Submit', self)
        self.button.move(20, 50)

        #Connect button to signal
        self.button.clicked.connect(self.on_button_clicked) 

        #Show the window
        self.show()

    def on_button_clicked(self):
        url = self.lineEdit.text()


app = QApplication(sys.argv)
window = MyWindow()
sys.exit(app.exec_())
