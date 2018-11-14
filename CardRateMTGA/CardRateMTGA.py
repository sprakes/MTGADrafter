import argparse
import cv2
from PIL import Image
import os
import pyautogui
from PyQt5 import QtCore, QtGui as qt, QtWidgets as qw
import sys
from pathlib import Path
from mtga.set_data import all_mtga_cards

class MainUI(qw.QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()
        #_mainWindow
        self.setGeometry(50, 50, 700, 500)
        self.setWindowTitle("MTGA Draft Bud")
        #_runButton
        self.runButton = qw.QPushButton('Get Draft Deck', self)
        self.runButton.setGeometry(50, 50, 70, 25)
        self.runButton.clicked.connect(lambda: runOCR())

def runOCR():
    pic = pyautogui.screenshot()
    print(os.getcwd())
    pic.save('temp.png')
    pic = cv2.imread('temp.png', 0)
    pic = cv2.threshold(pic, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    #pic = cv2.medianBlur(pic, 3)
    read_log_file_deck(False)

def read_log_file_deck(concurrent=True):
    card_list = []
    pth = str(Path.home()) + "\\AppData\\LocalLow\\Wizards Of The Coast\\MTGA\\output_log.txt"
    logfile = open(pth, "r")
    loglines = follow(logfile) if concurrent else simple_follow(logfile)
    watch_for_card_id = False
    for line in loglines:
        l = line.strip()
        if watch_for_card_id:
            if l.startswith("\"cardId\":"):
                cardID = l[11:-2]
                card_list.append((cardID, all_mtga_cards.lookup[int(cardID)]))
                watch_for_card_id = False
        elif l.startswith("Card picked:"):
            watch_for_card_id = True
    print("Your Draft Deck:")
    for card in card_list:
        print(card)

def main():
    app = qw.QApplication(sys.argv)
    ui = MainUI()
    ui.show()
    sys.exit(app.exec_())

# Follows the log file as it is being updated in game.
def follow(filee):
    filee.seek(0, 2)
    while True:
        line = filee.readline()
        if not line:
            time.sleep(0.1)
            continue
        elif line.strip() == "\"draftStatus\": \"Draft.Complete\",":
            break
        yield line


# Used to read from an already existing log file, as a test.
def simple_follow(filee):
    while True:
        line = filee.readline()
        if line:
            yield line
        else:
            break

if __name__ == "__main__":
    main()