from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon
import engine
from os import getlogin
import pathlib

#to get cmd line args
import sys

#TODO: for .mf unpacker, options should include "create vanilla dir", "to \contentpacks"
#TODO: for .mf unpacker, options should include which phase to unpack? checklist? in-client guide?

#dummy syscall to get taskbar icon LOL
import ctypes
myappid = 'shtickerpack' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

#create a custom subclassed window
class ShtickerpackMainWindow(QMainWindow):
    def __init__(self):
        #call the init method of QMainWindow
        super().__init__()

        self.setWindowTitle("shtickerpack alpha")
        self.setWindowIcon(QIcon("shtickerpack.png"))
        self.resize(1000, 415)

        self.mainContainer = QWidget()
        self.layout = QVBoxLayout()

        self.unpackPanel = ShtickerpackUnpackTray()
        self.unpackGroup = ShtickerpackTitledPanel(self.unpackPanel, "Unpack .mf files")
        self.layout.addWidget(self.unpackGroup)

        self.infoPanel = ShtickerpackProjectSetupTray()
        self.infoGroup = ShtickerpackTitledPanel(self.infoPanel, "Repacking instructions")
        self.infoGroup.setFixedHeight(120)
        self.layout.addWidget(self.infoGroup)

        self.inputFilePanel = ShtickerpackRepackTray()
        self.inputGroup = ShtickerpackTitledPanel(self.inputFilePanel, "Repack assets into .mf files")
        self.layout.addWidget(self.inputGroup)

        self.mainContainer.setLayout(self.layout)
        self.setCentralWidget(self.mainContainer)
        self.show()


class ShtickerpackTitledPanel(QGroupBox):
    def __init__(self, layout: QGridLayout, title: str):
        super().__init__(title) #sets title to identifier
        self.setLayout(layout)

class ShtickerpackProjectSetupTray(QGridLayout):
    def __init__(self, identifier: str = "ProjectSetupTray"):
        super().__init__()

        self.identifier = identifier
        self.helpLabel = QLabel(("Use the Unpack panel above to extract the asset files from Clash's phase files. " +
                                "Copy each file you'd like to change into a new folder (ex. <b><code>desktop/myContentPack/</code></b>). <br>"
                                "When you're happy with your changes, select that folder in the Repack Assets tray below. <br>" +
                                "shtickerpack will automatically place each file where it needs to go, " +
                                "pack your changes into a .mf file, and move it to <b><code>/Corporate Clash/resources/contentpacks/</code></b>. <br>" +
                                "Clash will automatically use any packed files in the <b><code>/contentpacks/</code></b> folder in-game. "+
                                "Simply remove any .mf file from this folder to disable it."))
        self.addWidget(self.helpLabel, 0, 0)

class ShtickerpackRepackTray(QGridLayout):
    def __init__(self, identifier: str = "RepackTray"):
        super().__init__()

        self.identifier = identifier
        self.DEFAULT_LOOSE_DIR = f"C:/Users/{getlogin()}/AppData/Local/Corporate Clash/resources/workspace/myProject" #TODO: really??
        self.DEFAULT_OUTPUT_DIR = f"C:/Users/{getlogin()}/AppData/Local/Corporate Clash/resources/contentpacks"

        self.inputDirHint = QLabel("Custom asset folder:")
        self.inputDirHint.setFixedWidth(150)
        self.inputDirPath = QLineEdit()
        self.inputBrowseButton = QPushButton("Select custom asset folder...")
        self.inputBrowseButton.clicked.connect(self.openInputFileDialog)
        self.defaultInputButton = QPushButton("Use default input folder")
        self.defaultInputButton.clicked.connect(self.setDefaultInputDir)
        self.defaultInputButton.setDisabled(True)

        self.modNameHint = QLabel("Output file name:")
        self.modNameHint.setFixedWidth(150)
        self.modNameEntry = QLineEdit()
        self.autoNameModButton = QPushButton("Choose a name for me")
        self.autoNameModButton.clicked.connect(lambda:self.modNameEntry.setText(self.generateRandomModName()))

        self.optionsSpacer = QHorizontalSpacer()

        self.delFolderModeBox = QCheckBox("Delete temporary folders when done")
        self.delFolderModeBox.clicked.connect(lambda:self.deleteModeWarning(self.delFolderModeBox))
        self.delFilesModeBox = QCheckBox("Delete asset files when done")
        self.delFilesModeBox.clicked.connect(lambda:self.deleteModeWarning(self.delFilesModeBox))
        self.moveOutputModeBox = QCheckBox("Move output to Clash resources when done (recommended)") #todo: warning when deselected
        self.moveOutputModeBox.setChecked(True)
        
        self.repackButton = QPushButton("Go!") #todo: implement, lol
        #self.repackButton.clicked.connect(lambda:self.unpackTargetDir(self.repackButton))

        self.addWidget(self.inputDirHint, 0, 0)
        self.addWidget(self.inputDirPath, 0, 1, 1, 2) #merge these elements to line up box w unpack label?
        self.addWidget(self.inputBrowseButton, 0, 3, 1, 1)

        self.addWidget(self.modNameHint, 1, 0)
        self.addWidget(self.modNameEntry, 1, 1, 1, 2) #merge these elements to line up box w unpack label?
        self.addWidget(self.autoNameModButton, 1, 3, 1, 1)

        self.addWidget(self.optionsSpacer, 2, 0, 1, 4)

        self.addWidget(self.delFilesModeBox, 3, 0, 1, 1)
        self.addWidget(self.delFolderModeBox, 3, 1, 1, 1)
        self.addWidget(self.moveOutputModeBox, 3, 2, 1, 2)
    
        self.addWidget(self.repackButton, 0, 4, 4, 1)
        self.repackButton.setMaximumHeight(999)
    
    def generateRandomModName(self):
        dirToCheck = self.DEFAULT_OUTPUT_DIR #.../clash/resources/contentpacks
        #TODO: should have logic to generate myMod(X) to avoid duplicates, but placehodler for now
        return "PlaceholderModName"
        

    def openInputFileDialog(self):
        dir = QFileDialog.getExistingDirectory(
            None,
            caption = "Select input phase file folder...",
            directory = f"C:/Users/{getlogin()}/AppData/Local/Corporate Clash/resources"
        )
        if dir:
            path = pathlib.Path(dir)
            self.inputDirPath.setText(str(path))
            print(f"Selected {path} in tray {self.identifier}")

    def setDefaultInputDir(self):
        self.inputDirPath.setText(self.DEFAULT_LOOSE_DIR)

    def deleteModeWarning(self, button: QCheckBox):
        msgData = { #folder, file
            False: {
                False: (None, None),
                True: (QMessageBox.warning, "This will delete your loose asset files once complete. They'll still be available in the generated phase folders and multifile. Is this OK?")
            },
            True: {
                False: (QMessageBox.warning, "This will delete generated folders once complete. Your asset files won't be deleted. Is this OK?"),
                True: (QMessageBox.critical, "This will delete loose asset files AND generated folders once complete. They'll still be available in the generated multifile, but you'll have to unpack it manually <b>(which can be annoying)</b>. Is this OK?")
            }
        }
        messageType, messageStr = msgData[self.delFolderModeBox.isChecked()][self.delFilesModeBox.isChecked()] #this is the best thing i have ever written
        if button.checkState():
            result = messageType(None, "Note!", messageStr, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
            if result == QMessageBox.StandardButton.No:
                button.setChecked(False)
                



class ShtickerpackUnpackTray(QGridLayout):
    def __init__(self, identifier: str = "UnpackTray"):
        super().__init__()

        self.identifier = identifier
        self.DEFAULT_INPUT_DIR = f"C:/Users/{getlogin()}/AppData/Local/Corporate Clash/resources/default"
        self.DEFAULT_OUTPUT_DIR = f"C:/Users/{getlogin()}/AppData/Local/Corporate Clash/resources/vanilla"

        self.inputDirHint = QLabel("Get phase files (.mf) from:")
        self.inputDirHint.setFixedWidth(150)
        self.inputDirPath = QLineEdit()
        self.inputBrowseButton = QPushButton("Select input folder...")
        self.inputBrowseButton.clicked.connect(self.openInputFileDialog)
        self.defaultInputButton = QPushButton("Use default input folder")
        self.defaultInputButton.clicked.connect(self.setDefaultInputDir)

        self.outputDirHint = QLabel("Place output folders in:")
        self.outputDirHint.setFixedWidth(150)
        self.outputDirPath = QLineEdit()
        self.outputBrowseButton = QPushButton("Select output folder...")
        self.outputBrowseButton.clicked.connect(self.openOutputFileDialog)
        self.defaultOutputButton = QPushButton("Use vanilla output folder")
        self.defaultOutputButton.clicked.connect(self.setDefaultOutputDir)

        self.defaultHybridButton = QPushButton("Use default folders (Recommended)")
        self.defaultHybridButton.clicked.connect(self.setDefaultInputDir)
        self.defaultHybridButton.clicked.connect(self.setDefaultOutputDir)
        
        self.unpackButton = QPushButton("Go!")
        self.unpackButton.clicked.connect(lambda:self.unpackTargetDir(self.unpackButton))

        self.addWidget(self.inputDirHint, 0, 0)
        self.addWidget(self.outputDirHint, 1, 0)
        self.addWidget(self.inputDirPath, 0, 1, 1, 2)
        self.addWidget(self.outputDirPath, 1, 1, 1, 2)

        self.addWidget(self.defaultHybridButton, 2, 0, 1, 4)
        self.addWidget(self.defaultInputButton, 3, 0, 1, 2)
        self.addWidget(self.defaultOutputButton, 3, 2, 1, 2)
        
        self.addWidget(self.inputBrowseButton, 0, 3)
        self.addWidget(self.outputBrowseButton, 1, 3)

        self.addWidget(self.unpackButton, 0, 4, 4, 1)
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
                #is this neccesary? not rn
                pass
                # msg = QMessageBox.warning(None, "de-multify error",
                #     "You already have a vanilla folder. Rename it or choose a different folder.")
                # return

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


class QHorizontalSpacer(QFrame):
    def __init__(self):
        super(QHorizontalSpacer, self).__init__()
        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)


#QApplication object is the app, sys.argv are the cmd line args
app = QApplication(sys.argv)

#create a widget (the window)
window = ShtickerpackMainWindow()
window.show() #need to explicitly show it, windows (w/o a visible parent) are hidden by default

#start the event loop
app.exec()




#reaches here once app exits and event loop stops