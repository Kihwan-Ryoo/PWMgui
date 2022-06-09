import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSlider, QSpinBox, QDesktopWidget, QLabel
from PyQt5.QtCore import Qt
import serial
import struct
import serial.tools.list_ports

def get_ports():
    ports = serial.tools.list_ports.comports()
    return ports

def findArduino(portsFound):
    commPort = 'None'
    numConnection = len(portsFound)
    for i in range(0, numConnection):
        port = foundPorts[i]
        strPort = str(port)
        if 'Arduino' in strPort:
            splitPort = strPort.split(' ')
            commPort = (splitPort[0])
    return commPort

foundPorts = get_ports()
connectPort = findArduino(foundPorts)

if connectPort != 'None':
    ser = serial.Serial(port=connectPort,
                        baudrate=9600,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS)
else:
    print('Connection Issue!')

print(ser.name)

class PCArduinoPWM(QWidget):
    def __init__(self, ser):
        super().__init__()
        self.initUI(ser)

    def initUI(self, ser):
        self.ser = ser

        self.slider = QSlider(Qt.Vertical, self)
        self.slider.setRange(0, 100)
        self.slider.setSingleStep(1)
        self.slider.setTickPosition(QSlider.TicksLeft)
        self.slider.setTickInterval(5)

        self.min = QLabel('0', self)
        self.min.setAlignment(Qt.AlignCenter)
        self.mid = QLabel('50', self)
        self.mid.setAlignment(Qt.AlignCenter)
        self.max = QLabel('100', self)
        self.max.setAlignment(Qt.AlignCenter)

        self.lcd = QSpinBox(self)
        self.lcd.setRange(0, 100)

        self.label = QLabel('label', self)

        self.slider.valueChanged.connect(self.lcd.setValue)
        self.lcd.valueChanged.connect(self.slider.setValue)
        self.slider.valueChanged.connect(self.ChangeValue)

        vbox_slider = QVBoxLayout()
        vbox_slider.addWidget(self.max)
        vbox_slider.addStretch(50)
        vbox_slider.addWidget(self.mid)
        vbox_slider.addStretch(50)
        vbox_slider.addWidget(self.min)

        hbox_slider = QHBoxLayout()
        hbox_slider.addStretch(1)
        hbox_slider.addLayout(vbox_slider)
        hbox_slider.addWidget(self.slider)
        hbox_slider.addStretch(1)

        hbox_spin = QHBoxLayout()
        hbox_spin.addStretch(1)
        hbox_spin.addWidget(self.lcd)
        hbox_spin.addWidget(self.label)
        hbox_spin.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(2)
        vbox.addLayout(hbox_slider, 100)
        vbox.addStretch(5)
        vbox.addLayout(hbox_spin, 100)
        vbox.addStretch(2)

        self.setLayout(vbox)

        self.setWindowTitle('MOTORpwm')
        self.resize(260, 400)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def ChangeValue(self, value):
        print(value)
        self.ser.write(struct.pack('>B', value))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PCArduinoPWM(ser)
    sys.exit(app.exec_())