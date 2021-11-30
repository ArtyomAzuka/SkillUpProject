from PyQt5 import QtWidgets
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice
from Interface import Ui_MainWindow

import sys

working = ''
last_ID = None
current_ID = None
identificators = []
is_key = False
comparison = None
key_ID = None
serial = QSerialPort()
serial.setBaudRate(9600)
portlist = [port.portName() for port in QSerialPortInfo.availablePorts()]
# print(portlist)
serial.setPortName(portlist[0])
serial.open(QIODevice.ReadWrite)


def reading():
    # print(3)
    global last_ID, current_ID, working, serial, identificators, key_ID, is_key
    rz = serial.readLine()
    ans = ''.join(str(rz, 'UTF-8').strip().split(' '))
    working += ans
    # print(rz)
    # print(working)
    if len(working) == 10:
        last_ID = current_ID
        current_ID = working[3::]
        # print(current_ID)
        # print(working)
        working = ''
        if is_key is False:
            identificators.append(current_ID)
        else:
            key_ID = current_ID
            is_key =  False
            # print(current_ID)


serial.readyRead.connect(reading)


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_2.clicked.connect(self.getID)
        self.ui.pushButton_3.clicked.connect(self.compareID)
        self.ui.pushButton.clicked.connect(self.start_key)

    def getID(self):
        global current_ID
        self.ui.label.setText(f"{current_ID}")

    def compareID(self):
        global comparison, serial, current_ID, last_ID, key_ID, identificators
        comparison = all([r == key_ID for r in identificators])
        serial.write((str(int(comparison)) + ';').encode())
        print(comparison, identificators)

    def start_key(self):
        global is_key
        is_key = True


app = QtWidgets.QApplication([])
application = mywindow()
application.show()
# serial.close()
sys.exit(app.exec())
