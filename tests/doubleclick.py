from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class ClickHandler():
    def __init__(self, time):
        self.timer = QtCore.QTimer()
        self.timer.setInterval(time)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.timeout)
        self.click_count = 0

    def timeout(self):
        if self.click_count == 1:
            print('Single click')
        elif self.click_count > 1:
            print('Double click')
        self.click_count = 0

    def __call__(self):
        self.click_count += 1
        if not self.timer.isActive():
            self.timer.start()


class MyDialog(QWidget):
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)

        self.button1 = QtGui.QPushButton("Button 1")
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.button1)
        self.setLayout(hbox)

        self.click_handler = ClickHandler(300)
        self.button1.clicked.connect(self.click_handler)

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    w = MyDialog()
    w.show()
    sys.exit(app.exec_())