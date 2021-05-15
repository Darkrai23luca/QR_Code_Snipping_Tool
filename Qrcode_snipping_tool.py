from PyQt5 import QtWidgets, QtCore, QtGui
from tkinter import *
from PIL import ImageGrab
import numpy as np
import cv2
from pyzbar.pyzbar import decode
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import Qrcode_snipping_Menu
import requests
import Output_Gui


class SnippingWidget(QtWidgets.QWidget):
    num_snip = 0
    is_snipping = False
    background = False
    flag = 0
    data = None
    image = []

    def __init__(self, parent=None):
        super(SnippingWidget, self).__init__()
        self.parent = parent

        self.root = Tk()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setGeometry(1, 1, screen_width, screen_height)
        self.setWindowIcon(QtGui.QIcon('qr_snipping_tool.ico'))
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.window_gui = None

    def start(self):

        SnippingWidget.background = False
        SnippingWidget.is_snipping = True
        self.setWindowOpacity(0.3)
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.show()

    def paintEvent(self, event):
        if SnippingWidget.is_snipping:
            brush_color = (128, 128, 255, 150)
            lw = 2
            opacity = 0.2
        else:
            # reset points, so the rectangle won't show up again.
            self.begin = QtCore.QPoint()
            self.end = QtCore.QPoint()
            brush_color = (0, 0, 0, 0)
            lw = 0
            opacity = 0

        self.setWindowOpacity(opacity)
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), lw))
        qp.setBrush(QtGui.QColor(*brush_color))
        rect = QtCore.QRectF(self.begin, self.end)
        qp.drawRect(rect)

    def URL_validator(self, data):
        try:
            print("In url " + data)
            requests.get(data)
            self.window_gui.UrlWindow(data)
        except requests.ConnectionError:
            print("URL does not exist on Internet")

    def QrCodeDecoder(self, image, status):
        self.image = image
        self.flag = status
        self.window_gui = Output_Gui.OutputGui()
        if self.image:
            self.data = None
            data = str(self.image[0].data).split("'")
            self.data = data[1]
            # print(self.data)

            if 'https:' in self.data[:6]:
                self.URL_validator(self.data)

            elif 'http:' in self.data[:6]:
                self.URL_validator(self.data)

            elif 'www.' in self.data[:6]:
                self.URL_validator(self.data)
            else:
                # print('Decoded data: ' + self.data)
                self.window_gui.TextWindow(self.data)

        else:
            self.window_gui.qrCodeShowDialog()
            # print("No QR code found")

        cv2.waitKey(0)
        cv2.destroyAllWindows()
        if self.flag == 2:
            self.close()

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        status = 2
        SnippingWidget.is_snipping = False
        QtWidgets.QApplication.restoreOverrideCursor()
        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        self.repaint()
        QtWidgets.QApplication.processEvents()
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))

        QtWidgets.QApplication.processEvents()
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
        img1 = decode(img)
        self.QrCodeDecoder(img1, status)
        Qrcode_snipping_Menu.Menu((x1, y1, x2, y2))
