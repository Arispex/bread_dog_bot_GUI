from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication
import sys
from models import MainWindow
import os

basedir = os.path.dirname(__file__)

try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'qianyiovo.bread.bog.bot'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

app = QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon(os.path.join(basedir, "logo.ico")))

window = MainWindow()
window.show()

app.exec()
