# This Python file uses the following encoding: utf-8
from PyQt5.QtNetwork import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("mainwindow.ui", self)

        self.connected = False
        self.socket = self.makeSocket()

        self.box_lineedit = QLineEdit(self)
        self.box_combobox.setLineEdit(self.box_lineedit)

        self.conectar_button.clicked.connect(self.onConectarButtonClicked)
        self.enviar_button.clicked.connect(self.onEnviarButtonClicked)
        self.actionSalir.triggered.connect(self.close)

    def onSocketReadyRead(self):
        self.connected = True
        msg = self.socket.readAll()
        msg = str(msg, "utf-8")
        self.estado_label.setText(msg)

    def makeSocket(self):
        socket = QTcpSocket(self)
        socket.readyRead.connect(self.onSocketReadyRead)
        return socket

    def onConectarButtonClicked(self):
        host = self.host_lineedit.text()
        port = int(self.puerto_lineedit.text())
        self.socket.disconnectFromHost()
        self.socket.connectToHost(host, port)

    def onEnviarButtonClicked(self):
        if not self.connected:
            return

        boxName = self.box_lineedit.text()
        height = self.height_lineedit.text()
        length = self.length_lineedit.text()
        width = self.width_lineedit.text()

        if boxName == "":
            return
        if height == "":
            return
        if length == "":
            return
        if width == "":
            return

        exists = False
        count = self.box_combobox.count()
        for x in range(count):
            currentText = self.box_combobox.itemText(x)
            if currentText == boxName:
                exists = True
                break

        data = "box(boxName:{},height:{},length:{},width:{},exists:{})".format(boxName, height, length, width, exists)
        self.socket.write(bytes(data, "utf-8"))

        if not exists:
            self.box_combobox.addItem(boxName)
