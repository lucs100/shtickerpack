from PyQt6.QtWidgets import *
import packer
from os import getlogin
import pathlib

#to get cmd line args
import sys

#create a custom subclassed window
class ShtickerpackMainWindow(QMainWindow):
    def __init__(self):
        #call the init method of QMainWindow
        super().__init__()

        self.setWindowTitle("CONFIDENTIAL jk lol")
        self.setFixedSize(600, 400)

        self.mainContainer = QWidget()
        self.layout = QVBoxLayout()

        self.inputFileLayout1 = ShtickerpackInputTray("top")
        self.inputFileLayout2 = ShtickerpackInputTray("middle")
        self.inputFileLayout3 = ShtickerpackInputTray("bottom")

        self.layout.addLayout(self.inputFileLayout1)
        self.layout.addLayout(self.inputFileLayout2)
        self.layout.addLayout(self.inputFileLayout3)
        self.mainContainer.setLayout(self.layout)
        self.setCentralWidget(self.mainContainer)
        self.show()


class ShtickerpackInputTray(QGridLayout):
    def __init__(self, identifier: str):
        super().__init__()

        self.identifier = identifier
        self.DEFAULT_INPUT_DIR = f"C:\\Users\\{getlogin()}\\AppData\\Local\\Corporate Clash\\Resources\\Default"

        self.inputDirEdit = QLineEdit()
        self.browseButton = QPushButton("Select input folder...")
        self.browseButton.clicked.connect(self.openInputFileDialog)
        self.defaultButton = QPushButton("Use default folder")
        self.defaultButton.clicked.connect(self.setDefaultInputDir)
        self.testButton = QPushButton("Use test folder")

        self.addWidget(QLabel("Phase file input location:"), 0, 0)
        self.addWidget(self.inputDirEdit, 1, 0, 1, 3)
        self.addWidget(self.browseButton, 0, 1)
        self.addWidget(self.defaultButton, 0, 2)
    
    def openInputFileDialog(self):
        dir = QFileDialog.getExistingDirectory(
            None,
            caption = "Select input phase file folder...",
            directory = f"C:/Users/{getlogin()}/AppData/Local/Corporate Clash/Resources/Default"
        )
        if dir:
            path = pathlib.Path(dir)
            self.inputDirEdit.setText(str(path))
            print(f"Selected {path} in tray {self.identifier}")

    def setDefaultInputDir(self):
        self.inputDirEdit.setText(self.DEFAULT_INPUT_DIR)


#QApplication object is the app, sys.argv are the cmd line args
app = QApplication(sys.argv)

#create a widget (the window)
window = ShtickerpackMainWindow()
window.show() #need to explicitly show it, windows (w/o a visible parent) are hidden by default

#start the event loop
app.exec()




#reaches here once app exits and event loop stops