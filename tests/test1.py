import sys
from PyQt5 import QtCore, QtWidgets

class Dialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Dialog, self).__init__()
        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.addItems('One Two Three'.split())
        self.listWidget.installEventFilter(self)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.listWidget)

    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.ContextMenu and
            source is self.listWidget):
            menu = QtWidgets.QMenu()
            menu.addAction('Open Window')
            if menu.exec_(event.globalPos()):
                item = source.itemAt(event.pos())
                print(item.text())
            return True
        return super(Dialog, self).eventFilter(source, event)

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = Dialog()
    window.setGeometry(600, 100, 300, 200)
    window.show()
    sys.exit(app.exec_())