from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class BoxAttributes(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.layout = QVBoxLayout()
        self.tabWidget = QTabWidget()
        self.setContentsMargins(0, 0, 0, 0)
        self.setGeometry(200, 500, 500, 200)
        self.setWindowTitle("Box Attributes")
        self.tabWidget.setFont(QFont("Ubuntu", 12))
        self.buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonbox.accepted.connect(self.accept)
        self.buttonbox.rejected.connect(self.reject)
        self.tabWidget.addTab(TabTest1(), "Test 1")
        self.tabWidget.addTab(TabTest2(), "Test 2")
        self.layout.addWidget(self.tabWidget)
        self.layout.addWidget(self.buttonbox)
        self.setLayout(self.layout)
        self.show()

class TabTest1(QWidget):
    def __init__(self):
        super().__init__()
        test_variable_1_label = QLabel("Test Variable 1: ")
        test_variable_1_edit = QLineEdit()
        test_variable_2_label = QLabel("Test Variable 2:")
        test_variable_2_edit = QLineEdit()
        layout = QVBoxLayout()
        layout.addWidget(test_variable_1_label)
        layout.addWidget(test_variable_1_edit)
        layout.addWidget(test_variable_2_label)
        layout.addWidget(test_variable_2_edit)
        self.setLayout(layout)

class TabTest2(QWidget):
    def __init__(self):
        super().__init__()
        test_variable_3_label = QLabel("Test Variable 3: ")
        test_variable_3_edit = QLineEdit()
        test_variable_4_label = QLabel("Test Variable 4:")
        test_variable_4_edit = QLineEdit()
        layout = QVBoxLayout()
        layout.addWidget(test_variable_3_label)
        layout.addWidget(test_variable_3_edit)
        layout.addWidget(test_variable_4_label)
        layout.addWidget(test_variable_4_edit)
        self.setLayout(layout)
