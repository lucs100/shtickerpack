from PyQt6.QtWidgets import *
import engine
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
        self.setFixedSize(1000, 300)

        self.mainContainer = QWidget()
        self.layout = QVBoxLayout()

        self.inputFilePanel1 = ShtickerpackInputTray("top")
        self.inputGroup1 = ShtickerpackTitledPanel(self.inputFilePanel1, "Input Panel 1")
        self.layout.addWidget(self.inputGroup1)

        self.inputFilePanel2 = ShtickerpackInputTray("bottom")
        self.inputGroup2 = ShtickerpackTitledPanel(self.inputFilePanel2, "Input Panel 2")
        self.layout.addWidget(self.inputGroup2)

        self.mainContainer.setLayout(self.layout)
        self.setCentralWidget(self.mainContainer)
        self.show()


class ShtickerpackTitledPanel(QGroupBox):
    def __init__(self, layout: QGridLayout, title: str):
        super().__init__(title) #sets title to identifier
        self.setLayout(layout)


class ShtickerpackInputTray(QGridLayout):
    def __init__(self, identifier: str):
        super().__init__()

        self.identifier = identifier
        self.DEFAULT_INPUT_DIR = f"C:/Users/{getlogin()}/AppData/Local/Corporate Clash/resources/default"
        self.DEFAULT_OUTPUT_DIR = f"C:/Users/{getlogin()}/AppData/Local/Corporate Clash/resources/vanilla"

        self.inputDirPath = QLineEdit()
        self.inputBrowseButton = QPushButton("Select input folder...")
        self.inputBrowseButton.clicked.connect(self.openInputFileDialog)
        self.defaultInputButton = QPushButton("Use default folder (Recommended)")
        self.defaultInputButton.clicked.connect(self.setDefaultInputDir)

        self.outputDirPath = QLineEdit()
        self.outputBrowseButton = QPushButton("Select output folder...")
        self.outputBrowseButton.clicked.connect(self.openOutputFileDialog)
        self.defaultOutputButton = QPushButton("Use vanilla folder (Recommended)")
        self.defaultOutputButton.clicked.connect(self.setDefaultOutputDir)
        
        self.unpackButton = QPushButton("Go!")
        self.unpackButton.clicked.connect(lambda:self.unpackTargetDir(self.unpackButton))

        self.addWidget(QLabel("Get phase files (.mf) from:"), 0, 0)
        self.addWidget(QLabel("Place phase folders in:"), 1, 0)
        self.addWidget(self.inputDirPath, 0, 1, 1, 2)
        self.addWidget(self.outputDirPath, 1, 1, 1, 2)

        self.addWidget(self.defaultInputButton, 2, 0, 1, 2)
        self.addWidget(self.defaultOutputButton, 2, 2, 1, 2)
        
        self.addWidget(self.inputBrowseButton, 0, 3)
        self.addWidget(self.outputBrowseButton, 1, 3)

        self.addWidget(self.unpackButton, 0, 4, 3, 1)
        self.unpackButton.setMaximumHeight(999)
    
    def openInputFileDialog(self):
        dir = QFileDialog.getExistingDirectory(
            None,
            caption = "Select input phase file folder...",
            directory = f"C:/Users/{getlogin()}/AppData/Local/Corporate Clash/resources/default"
        )
        if dir:
            path = pathlib.Path(dir)
            self.inputDirPath.setText(str(path))
            print(f"Selected {path} in tray {self.identifier}")

    def openOutputFileDialog(self):
        dir = QFileDialog.getExistingDirectory(
            None,
            caption = "Select output phase file folder...",
            directory = f"C:/Users/{getlogin()}/AppData/Local/Corporate Clash/resources"
        )
        if dir:
            path = pathlib.Path(dir)
            self.outputDirPath.setText(str(path))
            print(f"Selected {path} in tray {self.identifier}")

    def setDefaultInputDir(self):
        self.inputDirPath.setText(self.DEFAULT_INPUT_DIR)

    def setDefaultOutputDir(self):
        self.outputDirPath.setText(self.DEFAULT_OUTPUT_DIR)
    
    def unpackTargetDir(self, button: QPushButton): #async? lots of extra logic 
        #this is a mess already
        if self.inputDirPath.text() == "":
            self.inputDirPath.setText(self.DEFAULT_INPUT_DIR)
        if self.outputDirPath.text() in ["", self.DEFAULT_OUTPUT_DIR]: #force vanilla dupe case
            self.outputDirPath.setText(self.DEFAULT_OUTPUT_DIR)
            if not engine.prepDir(self.DEFAULT_OUTPUT_DIR):
                #is this neccesary?
                msg = QMessageBox.warning(None, "de-multify error",
                    "You already have a vanilla folder. Rename it or choose a different folder")
                return

        target_dir = self.inputDirPath.text()
        destination_dir = self.outputDirPath.text()

        if engine.checkOutputDirectoryValid(destination_dir):
            button.setText("Unpacking... just a sec!")
            engine.unpackDirectory(target_dir, destination_dir)
            msg = QMessageBox.information(None, "de-multify", "Folder unpacked!")
            button.setText("Go!")
        else:
            msg = QMessageBox.critical(None, "de-multify error", 
                "The output folder doesn't exist or already has phase folders inside!")




#QApplication object is the app, sys.argv are the cmd line args
app = QApplication(sys.argv)

#create a widget (the window)
window = ShtickerpackMainWindow()
window.show() #need to explicitly show it, windows (w/o a visible parent) are hidden by default

#start the event loop
app.exec()




#reaches here once app exits and event loop stops