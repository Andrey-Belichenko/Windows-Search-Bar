import sys

import json

import webbrowser
from googlesearch import search

import subprocess

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QLineEdit, QVBoxLayout, QMessageBox
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import Qt, QPoint, pyqtSlot, QUrl


def load_json_path():
    with open('conf.json') as json_file:
        paths = json.load(json_file)
    return paths


conf = load_json_path()     # load config json string from conf.json


class SearchWin(QWidget):
    """
    Class for searching window, what will raising if you use "search_in_web" func
    """
    def __init__(self, link):
        super().__init__()
        self.browser = None
        self.link = link
        self.opacity = 0.5
        self.width = 800
        self.height = 600
        self.top = 60
        self.left = int(app.primaryScreen().size().width() / 2) - int(self.width / 2)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Browser")
        self.browser = QWebEngineView()
        self.browser.load(QUrl(self.link))
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowOpacity(self.opacity)
        lay = QVBoxLayout(self)
        lay.addWidget(self.browser)


class Bar(QMainWindow):
    """
    The class of the base command line of the program
    """
    def __init__(self):
        super().__init__()
        self.commands = {
                         "start game": "start_game",
                         "start chatting": "self.start_chatting",
                         "start browsing": "start_browsing",
                         "find": "search_in_web",
                         "search": "search_in_web"
                         }
        self.query = ""
        self.win = None
        self.text = ""
        self.opacity = 0.5
        self.title = "Bar"
        self.width = 350
        self.height = 27
        self.left = int(app.primaryScreen().size().width() / 2) - int(self.width / 2)
        self.top = 0
        self.press = False
        self.last_pos = QPoint(0, 0)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowOpacity(self.opacity)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(0, 1)
        self.textbox.resize(280, 25)

        # Create a button in the window
        self.button = QPushButton('Go', self)
        self.button.move(280, 0)
        self.button.resize(50, 28)

        # connect button to function on_click
        self.button.clicked.connect(self.on_click)
        self.show()

    @pyqtSlot()
    def on_click(self):
        self.command_handler()

    def mouseMoveEvent(self, event):
        if self.press:
            self.move(event.globalPos() - self.last_pos)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.press = True

        self.last_pos = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.press = False

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

        if e.key() == Qt.Key_Return:
            self.command_handler()
            # textbox_value = self.textbox.text()
            # QMessageBox.question(self, 'BarApp', "You typed: " + textbox_value, QMessageBox.Ok,
            #                      QMessageBox.Ok)
            # self.textbox.setText("")

    def search_in_web(self):
        """
        Search on the Internet for a request from a user
        Rise the second win with results
        """
        print("start search")
        link_list = []
        link_gen_obj = search(self.query, tld="co.in", num=1, stop=1, pause=2)  # getting search request
        for elem in link_gen_obj:
            link_list.append(elem)
        self.win = SearchWin(link_list[0])
        self.win.show()

    def not_command(self):
        """
        Raise QMassageBox "Not a command"
        :return:
        """
        QMessageBox.question(self, 'Bar', " Warning: Not s command ", QMessageBox.Ok, QMessageBox.Ok)


    @staticmethod
    def start_game():
        """
        Method start steam and discord and steam apps and start music page if music_flag is 1 in conf
        """

        subprocess.call(conf["steam_path"])
        subprocess.call(conf["discord_path"])
        if conf["music_flag"] == 1:
            webbrowser.open_new_tab(conf["music_page"])

    @staticmethod
    def start_browsing():
        """
        Method start your default browser app
        """
        webbrowser.open_new_tab(conf["browser_home_page"])

    @staticmethod
    def start_chatting():
        """
        Method start discord, browser and start music page if music_flag is 1 in conf
        """

        subprocess.call(conf["discord_path"])
        webbrowser.open(conf["browser_home_page"])
        if conf["music_flag"] == 1:
            webbrowser.open_new_tab(conf["music_page"])

    def command_handler(self):
        """
        Splits the line into a command and an argument. Selects a command
        """
        self.text = self.textbox.text()
        exec_command_flag = 0

        for command in list(self.commands.keys()):
            if self.text.find(command) != -1:
                self.query = self.text.replace(command, "")         # Getting the "raw" command input
                func_name = "self." + self.commands[command] + "()"       # Make "raw" command looks like self.command()
                exec(func_name)
                exec_command_flag = 1
        if not exec_command_flag:
            self.not_command()
        self.text = ""


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = Bar()
    w.show()

    sys.exit(app.exec_())
