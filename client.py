from PyQt6.QtWidgets import *
import packer
from os import getlogin
import pathlib

#to get cmd line args
import sys

#TODO: for .mf unpacker, options should include "create vanilla dir", "to \contentpacks"
#TODO: for .mf unpacker, options should include which phase to unpack? checklist? in-client guide?

#create a custom subclassed window
class ShtickerpackMainWindow(QMainWindow):
    def __init__(self):
        #call the init method of QMainWindow
        super().__init__()

        self.setWindowTitle("CONFIDENTIAL jk lol")
        self.setFixedSize(700, 100)

        self.mainContainer = QWidget()
        self.layout = QVBoxLayout()

        self.inputFileLayout1 = ShtickerpackInputTray("top")
        # self.inputFileLayout2 = ShtickerpackInputTray("middle")
        # self.inputFileLayout3 = ShtickerpackInputTray("bottom")

        self.layout.addLayout(self.inputFileLayout1)
        # self.layout.addLayout(self.inputFileLayout2)
        # self.layout.addLayout(self.inputFileLayout3)
        self.mainContainer.setLayout(self.layout)
        self.setCentralWidget(self.mainContainer)
        self.show()


class ShtickerpackInputTray(QGridLayout):
    def __init__(self, identifier: str):
        super().__init__()

        self.identifier = identifier
        self.DEFAULT_INPUT_DIR = f"C:/Users/{getlogin()}/AppData/Local/Corporate Clash/resources/default"

        self.inputDirEdit = QLineEdit()
        self.browseButton = QPushButton("Select input folder...")
        self.browseButton.clicked.connect(self.openInputFileDialog)
        self.defaultButton = QPushButton("Use default folder")
        self.defaultButton.clicked.connect(self.setDefaultInputDir)
        self.testButton = QPushButton("Use test folder")
        self.unpackButton = QPushButton("Unpack!")
        self.unpackButton.clicked.connect(self.unpackTargetDir)

        self.addWidget(QLabel("Input phase file (.mf) location:"), 0, 0)
        self.addWidget(self.inputDirEdit, 0, 1, 1, 2)
        self.addWidget(self.browseButton, 1, 0)
        self.addWidget(self.defaultButton, 1, 1)
        self.addWidget(self.unpackButton, 1, 2)
    
    def openInputFileDialog(self):
        dir = QFileDialog.getExistingDirectory(
            None,
            caption = "Select input phase file folder...",
            directory = f"C:/Users/{getlogin()}/AppData/Local/Corporate Clash/resources/default"
        )
        if dir:
            path = pathlib.Path(dir)
            self.inputDirEdit.setText(str(path))
            print(f"Selected {path} in tray {self.identifier}")

    def setDefaultInputDir(self):
        self.inputDirEdit.setText(self.DEFAULT_INPUT_DIR)
    
    def unpackTargetDir(self, state: bool, target_dir: str = None, destination_dir: str = None): #async? lots of extra logic
        if target_dir is None:          target_dir = self.inputDirEdit.text()
        if destination_dir is None:     destination_dir = target_dir
        packer.unpackDirectory(target_dir, destination_dir)
        msg = QMessageBox()
        msg.setWindowTitle("de-multify")
        msg.setText("Directory unpacked!")
        msg.exec()


#QApplication object is the app, sys.argv are the cmd line args
app = QApplication(sys.argv)

#create a widget (the window)
window = ShtickerpackMainWindow()
window.show() #need to explicitly show it, windows (w/o a visible parent) are hidden by default

#start the event loop
app.exec()




#reaches here once app exits and event loop stops