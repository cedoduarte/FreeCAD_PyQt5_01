# This Python file uses the following encoding: utf-8
import sys
from PyQt5.QtWidgets import QApplication
from mainwindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
