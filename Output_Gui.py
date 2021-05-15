from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import webbrowser


class OutputGui(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(OutputGui, self).__init__()
        self.parent = parent
        self.box = None
        self.textbox = None
        self.setWindowIcon(QtGui.QIcon('qr_snipping_tool.ico'))

    def UrlWindow(self, data):
        title = 'URL Data'
        left_v = 900
        top = 300
        width = 320
        height = 130
        self.setWindowTitle(title)
        self.setGeometry(left_v, top, width, height)
        self.box = QLineEdit(self)
        self.box.move(27, 30)
        self.box.resize(280, 40)
        self.box.setText(data)
        button = QPushButton('Open Browser', self)
        button.setToolTip('Opens your default Browser')
        button.move(120, 90)
        button.clicked.connect(self.OnUrlClick)
        self.show()

    @pyqtSlot()
    def OnUrlClick(self):
        textboxValue = self.box.text()
        webbrowser.open(textboxValue, new=2)
        self.box.setText("")
        self.close()

    def TextWindow(self, data):
        title = 'Text Data'
        left_v = 900
        top = 300
        width = 370
        height = 150
        self.setWindowTitle(title)
        self.setGeometry(left_v, top, width, height)
        box = QVBoxLayout()
        self.textbox = QTextEdit()
        box.addWidget(self.textbox)
        self.textbox.setText("")
        self.textbox.setText(data)
        button = QPushButton('Copy text')
        button.setToolTip('Copies your text')
        box.addWidget(button)
        button.clicked.connect(self.OnTextClick)
        self.setLayout(box)

        self.show()

    @pyqtSlot()
    def OnTextClick(self):
        self.textbox.copy()
        self.close()

    def qrCodeShowDialog(self):
        QMessageBox.warning(self, 'QR Search failed', "No QR Code Found?", QMessageBox.Ok)
