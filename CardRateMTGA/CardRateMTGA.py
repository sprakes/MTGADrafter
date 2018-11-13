import argparse
import cv2
from PIL import Image
import os
import pyautogui
from PyQt5 import QtCore, QtGui as qt, QtWidgets as qw
import sys

class MainUI(qw.QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()
        #_mainWindow
        self.setGeometry(50, 50, 700, 500)
        self.setWindowTitle("MTGA Draft Bud")
        #_runButton
        self.runButton = qw.QPushButton('DO IT', self)
        self.runButton.setGeometry(50, 50, 70, 25)
        self.runButton.clicked.connect(lambda: runOCR())

def runOCR():
    pic = pyautogui.screenshot()
    print(os.getcwd())
    pic.save('temp.png')
    pic = cv2.imread('temp.png', 0)
    pic = cv2.threshold(pic, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    #pic = cv2.medianBlur(pic, 3)
    print("fuers")

def main():
    app = qw.QApplication(sys.argv)
    ui = MainUI()
    ui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()