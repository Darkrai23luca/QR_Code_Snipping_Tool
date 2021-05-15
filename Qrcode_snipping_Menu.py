"""
This is a Main File.
"""
import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QAction, QMainWindow, QApplication
import Qrcode_snipping_tool
import numpy as np
import pyautogui
from pyzbar.pyzbar import decode
import cv2
import Output_Gui


class Menu(QMainWindow):
    default_title = "QR Code Snipping Tool"
    frame = []

    def __init__(self, start_position=(500, 500, 400, 60)):
        super().__init__()

        self.title = Menu.default_title
        self.setWindowIcon(QtGui.QIcon('qr_snipping_tool.ico'))
        # scan snip
        new_scan_action = QAction('Scan', self)
        new_scan_action.setShortcut('Shift+V')
        new_scan_action.setStatusTip('Scan!')
        new_scan_action.triggered.connect(self.scan)

        # Snip & Scan snip
        new_snip_action = QAction('Snip Scan', self)
        new_snip_action.setShortcut('Ctrl+N')
        new_snip_action.setStatusTip('Snip!')
        new_snip_action.triggered.connect(self.new_image_window)

        # Exit
        exit_window = QAction('Exit', self)
        exit_window.setShortcut('Ctrl+Q')
        exit_window.setStatusTip('Exit application')
        exit_window.triggered.connect(self.close)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(new_scan_action)
        self.toolbar.addAction(new_snip_action)

        self.toolbar.addAction(exit_window)

        self.snippingTool = Qrcode_snipping_tool.SnippingWidget()
        self.setGeometry(*start_position)
        self.change_and_set_title(Menu.default_title)

    # snippingTool.start() will open a new window, so if this is the first snip, close the first window.
    def new_image_window(self):
        if self.snippingTool.background:
            self.close()
        self.snippingTool.start()

    def scan(self):
        status = 1
        image = pyautogui.screenshot()
        self.frame = np.array(image)
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        img = decode(self.frame)
        self.snippingTool.QrCodeDecoder(img, status)

    def change_and_set_title(self, new_title):
        self.title = new_title
        self.setWindowTitle(self.title)

    def closeEvent(self, event):
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainMenu = Menu()
    ex = Output_Gui.OutputGui()
    mainMenu.show()
    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_())
