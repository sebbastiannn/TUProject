import sys
from PyQt5.QtWidgets import *

from Editor.editor_window import EditorWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)

    wnd = EditorWindow()
    wnd.show()

    sys.exit(app.exec_())

