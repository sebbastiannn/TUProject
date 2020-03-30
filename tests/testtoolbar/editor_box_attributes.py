from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from tests.testtoolbar.editor_box import Box

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
        self.tabWidget.addTab(TabContact(), "Contact Details")
        self.tabWidget.addTab(TabPeronsalDetails(), "Personal Details")
        self.layout.addWidget(self.tabWidget)
        self.layout.addWidget(self.buttonbox)
        self.setLayout(self.layout)
        self.show()

class TabContact(QWidget):
    def __init__(self):
        super().__init__()
        capacityLabel = QLabel("Capacity: ")
        capacityEdit = QLineEdit()
        phone = QLabel("Phone:")
        phoneedit = QLineEdit()
        addr = QLabel("Address:")
        addredit = QLineEdit()
        email = QLabel("Email:")
        emailedit = QLineEdit()
        layouto = QVBoxLayout()
        layouto.addWidget(capacityLabel)
        layouto.addWidget(capacityEdit)
        layouto.addWidget(phone)
        layouto.addWidget(phoneedit)
        layouto.addWidget(addr)
        layouto.addWidget(addredit)
        layouto.addWidget(email)
        layouto.addWidget(emailedit)
        self.setLayout(layouto)


class TabPeronsalDetails(QWidget):
    def __init__(self):
        super().__init__()
        groupBox = QGroupBox("Select Your Gender")
        list = ["Male", "Female"]
        combo = QComboBox()
        combo.addItems(list)
        layout = QVBoxLayout()
        layout.addWidget(combo)
        groupBox.setLayout(layout)
        groupBox2 = QGroupBox("Select Your Favorite Programming Language")
        python = QCheckBox("Python")
        cpp = QCheckBox("C++")
        java = QCheckBox("Java")
        csharp = QCheckBox("C#")
        layoutp = QVBoxLayout()
        layoutp.addWidget(python)
        layoutp.addWidget(cpp)
        layoutp.addWidget(java)
        layoutp.addWidget(csharp)
        groupBox2.setLayout(layoutp)
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(groupBox)
        mainLayout.addWidget(groupBox2)
        self.setLayout(mainLayout)
