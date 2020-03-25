import sys


from PyQt5.QtWidgets import *

from tests.testtoolbar.editor_window import Window


if __name__ == '__main__':
    app = QApplication(sys.argv)

    wnd = Window()
    wnd.editor.addBoxes()
    wnd.show()

    sys.exit(app.exec_())
