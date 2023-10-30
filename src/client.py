#from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget, QGroupBox, QGridLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QCheckBox, QSizePolicy, QFrame, QApplication
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QObject, QThread, pyqtSignal
import engine, os, pathlib, debugpy
from subprocess import CalledProcessError

#to get cmd line args
import sys

#TODO: for .mf unpacker, options should include "create vanilla dir", "to \contentpacks"
#TODO: for .mf unpacker, options should include which phase to unpack? checklist? in-client guide?

#dummy syscall to get taskbar icon LOL
try:
    import ctypes
    myappid = 'lucs100.shtickerpack' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

UNPACK_HELP_STR = ("Clash stores its resource files as <i>phase files</i>, in <b><code>.mf</b></code> files (known as multifiles). " +
                   "They're stored in the <b><code>/Corporate Clash/resources/default/</b></code> folder. <br>" +
                   "Unless you installed Clash in a custom location, click <i>Use default folders</i> " +
                   "to automatically locate these folders and unpack the base game's assets. <br>" +
                   "By default, shtickerpack will unpack these files into <b><code>/Corporate Clash/resources/vanilla/</b></code>, " +
                   "but you can choose any output folder if you'd like. <br>"+
                   "<b>Advanced</b>: You can unpack any .mf file using shtickerpack, but keep in mind this will unpack ALL .mf files in the folder you select.")

REPACK_HELP_STR = ("Once you've unpack the phase files, you can change files and repack them into a mod. " +
                   "Copy each file you'd like to change into a new folder (ex. <b><code>desktop/myContentPack/</code></b>). <br>"
                   "Once you're happy with your changes, select the folder with your changed files in the Repack Assets tray below. <br>" +
                   "shtickerpack will automatically pack your changes into a mod as an a .mf file, " +
                   "and move it to <b><code>/Corporate Clash/resources/contentpacks/</code></b>. <br>" +
                   "Clash will automatically use any packed files in the <b><code>/contentpacks/</code></b> folder in-game. "+
                   "Simply remove any .mf file from this folder to disable it.")

APP_NAME = "repacker"
ORG_NAME = "lucs100"
APP_VER = "1.1"

#create a custom subclassed window
class ShtickerpackMainWindow(QMainWindow):
    def __init__(self):
        #call the init method of QMainWindow
        super().__init__()

        self.setWindowTitle(f"{APP_NAME} v{APP_VER}")
        if getattr(sys, 'frozen', False):
            iconPath = os.path.join(sys._MEIPASS, "./src/assets/shtickerpack.png")
        else: iconPath = "./assets/shtickerpack.png"
        print(iconPath)
        self.setWindowIcon(QIcon(iconPath))
        self.setFixedSize(1000, 375) #minimal height

        self.mainContainer = QWidget()
        self.layout = QVBoxLayout()

        #impl tab switcher?

        self.tabs = QTabWidget()
        self.tabs.resize(1000, 500)

        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.unpackInfoPanel = ShtickerpackInfoTray(UNPACK_HELP_STR)
        self.unpackInfoGroup = ShtickerpackTitledPanel(self.unpackInfoPanel, "Unpacking Instructions")
        self.unpackInfoGroup.setFixedHeight(110)
        self.unpackPanel = ShtickerpackUnpackTray(self)
        self.unpackGroup = ShtickerpackTitledPanel(self.unpackPanel, "Unpack .mf files")
        self.tab1.layout = QVBoxLayout()
        self.tab1.layout.addWidget(self.unpackInfoGroup)
        self.tab1.layout.addWidget(self.unpackGroup)
        self.tab1.setLayout(self.tab1.layout)
        self.tabs.addTab(self.tab1, "Unpack")

        self.repackInfoPanel = ShtickerpackInfoTray(REPACK_HELP_STR)
        self.repackInfoGroup = ShtickerpackTitledPanel(self.repackInfoPanel, "Repacking Instructions")
        self.repackInfoGroup.setFixedHeight(110)
        self.repackFilePanel = ShtickerpackRepackTray(self)
        self.repackGroup = ShtickerpackTitledPanel(self.repackFilePanel, "Repack assets into .mf files")
        self.tab2.layout = QVBoxLayout()
        self.tab2.layout.addWidget(self.repackInfoGroup)
        self.tab2.layout.addWidget(self.repackGroup)
        self.tab2.setLayout(self.tab2.layout)
        self.tabs.addTab(self.tab2, "Repack")

        self.layout.addWidget(self.tabs)
        self.mainContainer.setLayout(self.layout)
        self.setCentralWidget(self.mainContainer)
        self.show()

class ShtickerpackTitledPanel(QGroupBox):
    def __init__(self, layout: QGridLayout, title: str):
        super().__init__(title) #sets title to identifier
        self.setLayout(layout)

class ShtickerpackInfoTray(QGridLayout):
    def __init__(self, helpLabel: str, identifier: str = "InfoTray"):
        super().__init__()

        self.identifier = identifier
        self.helpLabel = QLabel(helpLabel)
        self.addWidget(self.helpLabel, 0, 0)

class ShtickerpackUnpackTray(QGridLayout):
    def __init__(self, parentWindow: QMainWindow, identifier: str = "UnpackTray"):
        super().__init__()

        self.parentWindow = parentWindow
        self.identifier = identifier
        self.DEFAULT_INPUT_DIR = f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Corporate Clash\\resources\\default"
        self.DEFAULT_OUTPUT_DIR = f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Corporate Clash\\resources\\vanilla"

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
        self.unpackButton.setFixedSize(189, 121)
        self.unpackButton.clicked.connect(lambda:self.unpackTargetDir(self.unpackButton))
        #print(f"Unpack - H: {self.unpackButton.height()}, W: {self.unpackButton.width()}")

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

        self.setContentsMargins(8, 16, 8, 16)
    
    def openInputFileDialog(self):
        dir = QFileDialog.getExistingDirectory(
            None,
            caption = "Select input phase file folder...",
            directory = f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Corporate Clash\\resources\\default"
        )
        if dir:
            path = pathlib.Path(dir)
            self.inputDirPath.setText(str(path))
            print(f"Selected {path} in tray {self.identifier}")

    def openOutputFileDialog(self):
        dir = QFileDialog.getExistingDirectory(
            None,
            caption = "Select output phase file folder...",
            directory = f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Corporate Clash\\resources"
        )
        if dir:
            path = pathlib.Path(dir)
            self.outputDirPath.setText(str(path))
            print(f"Selected {path} in tray {self.identifier}")

    def setDefaultInputDir(self):
        self.inputDirPath.setText(self.DEFAULT_INPUT_DIR)

    def setDefaultOutputDir(self):
        self.outputDirPath.setText(self.DEFAULT_OUTPUT_DIR)
    
    def handlePathErrors(self, inputPath: str, outputPath: str) -> bool:
        if inputPath == "":
            msg = QMessageBox.warning(None, "No input!", "Select an input folder first.")
            return False
        if outputPath == "":
            msg = QMessageBox.warning(None, "No outut!", "Select an output folder first.")
            return False
        if inputPath == outputPath:
            msg = QMessageBox.warning(None, "Warning!", "The input and output folders can't be the same.")
            return False
        return True
    
    def handleUnpackResult(self, result: "ThreadResult"):
        result.messageType(None, result.title, result.text)
    
    def unpackTargetDir(self, button: QPushButton):
        sourceDir = self.inputDirPath.text()
        destinationDir = self.outputDirPath.text()

        if not self.handlePathErrors(sourceDir, destinationDir):
            return False
        
        if not os.path.exists(destinationDir):
            os.mkdir(destinationDir)

        if not engine.checkOutputDirectoryValid(destinationDir):
            msg = QMessageBox.warning(None, "Alert!", 
                "The output folder doesn't exist or already has phase folders inside!")
            return
        
        #checks ok, we can proceed
        button.setText("Unpacking... just a sec!")
        print("Beginning unpack...")
        button.setEnabled(False)

        self.thread = QThread()
        self.worker = UnpackWorker(sourceDir=sourceDir, destinationDir=destinationDir)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.success.connect(self.thread.quit)
        self.thread.finished.connect(self.worker.deleteLater)
        self.worker.result.connect(self.handleUnpackResult)
        self.thread.start()
        
        #setup triggers for when thread is done
        self.thread.finished.connect(
            lambda: button.setEnabled(True)
        )
        self.thread.finished.connect(
            lambda: button.setText("Go!")
        )
        

class ShtickerpackRepackTray(QGridLayout):
    def __init__(self, parentWindow: QMainWindow, identifier: str = "RepackTray"):
        super().__init__()

        self.parentWindow = parentWindow
        self.identifier = identifier
        self.DEFAULT_LOOSE_DIR = f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Corporate Clash\\resources\\workspace\\myProject" #TODO: really??
        self.DEFAULT_OUTPUT_DIR = f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Corporate Clash\\resources\\contentpacks"

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
        self.autoNameModButton = QPushButton("Auto-set (Not recommended)")
        self.autoNameModButton.clicked.connect(lambda:self.modNameEntry.setText(self.generateRandomModName()))

        self.optionsSpacer = QHorizontalSpacer()
        self.delFoldersModeBox = QCheckBox("Delete temporary folders when done")
        self.delFoldersModeBox.clicked.connect(lambda:self.deleteModeWarning(self.delFoldersModeBox))
        self.delFilesModeBox = QCheckBox("Delete asset files when done")
        self.delFilesModeBox.clicked.connect(lambda:self.deleteModeWarning(self.delFilesModeBox))
        self.moveOutputModeBox = QCheckBox("Move output to Clash resources (recommended)") #todo: warning when deselected
        self.moveOutputModeBox.setChecked(True)

        self.optionsTray = QWidget()
        self.optionsTray.layout = QGridLayout()
        self.optionsTray.layout.addWidget(self.optionsSpacer, 0, 0, 1, 3)
        self.optionsTray.layout.addWidget(self.delFoldersModeBox, 1, 0)
        self.optionsTray.layout.addWidget(self.delFilesModeBox, 1, 1)
        self.optionsTray.layout.addWidget(self.moveOutputModeBox, 1, 2)
        self.optionsTray.setLayout(self.optionsTray.layout)
        self.optionsTray.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        
        self.repackButton = QPushButton("Go!") #todo: implement, lol
        self.repackButton.clicked.connect(lambda:self.repackTargetDir(self.repackButton))
        self.repackButton.setFixedSize(189, 121)
        #print(f"Repack - H: {self.repackButton.height()}, W: {self.repackButton.width()}")

        self.addWidget(self.inputDirHint, 0, 0)
        self.addWidget(self.inputDirPath, 0, 1, 1, 2) #merge these elements to line up box w unpack label?
        self.addWidget(self.inputBrowseButton, 0, 3, 1, 1)

        self.addWidget(self.modNameHint, 1, 0)
        self.addWidget(self.modNameEntry, 1, 1, 1, 2) #merge these elements to line up box w unpack label?
        self.addWidget(self.autoNameModButton, 1, 3, 1, 1)

        # self.addWidget(self.delFilesModeBox, 3, 0, 1, 1)
        # self.addWidget(self.delFolderModeBox, 3, 1, 1, 1)
        # self.addWidget(self.moveOutputModeBox, 3, 2, 1, 2)
        self.addWidget(self.optionsTray, 2, 0, 1, 4)

        self.addWidget(self.repackButton, 0, 4, 3, 1)
        self.repackButton.setMaximumHeight(999)
        #TODO: resize to match unpack go button size
        
        self.setContentsMargins(8, 16, 8, 16)
    
    def generateRandomModName(self):
        output = self.DEFAULT_OUTPUT_DIR #.../clash/resources/contentpacks
        placeholderName = "myShtickerpackMod"
        if not engine.modExists(output, placeholderName): return placeholderName
        i = 1 #ugly
        while True:
            if not engine.modExists(output, placeholderName+str(i)): 
                return (placeholderName+str(i))     
            else: i += 1   

    def openInputFileDialog(self):
        dir = QFileDialog.getExistingDirectory(
            None,
            caption = "Select input phase file folder...",
            directory = f"C:\\Users\\{os.getlogin()}"
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
                True: (QMessageBox.critical, "This will delete loose asset files AND generated folders once complete. They'll still be available in the generated multifile, but you'll have to unpack it or with shtickerpack <b>(which can be annoying)</b>. Is this OK?")
            }
        }
        messageType, messageStr = msgData[self.delFoldersModeBox.isChecked()][self.delFilesModeBox.isChecked()] #this is the best thing i have ever written
        if button.isChecked() and messageType is not None:
            result = messageType(None, "Note!", messageStr, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
            if result == QMessageBox.StandardButton.No:
                button.setChecked(False)
    
    def handleRepackResultData(self, repackResult: engine.phasePackOverallResult):
        if not repackResult.isClean():
            #messy, but how do you refactor this?? probably easier to just be explicit
            if (level4Files := repackResult.getFilesAtLevel(4)) is not None:
                msg4 = QMessageBox.warning(None, "Warning!", f"Shtickerpack skipped the following files:\n\n{level4Files}\n\nThis file doesn't seem to be part of Clash's resources. If you're sure this is a mistake, let me know on Github.")
            if (level3Files := repackResult.getFilesAtLevel(3)) is not None:
                msg3 = QMessageBox.critical(None, "Warning!", f"Shtickerpack skipped the following files:\n\n{level3Files}\n\nClash has multiple different files with these names, so shtickerpack can't tell which one you mean right now. This will be added eventually - let me know on GitHub that you ran into this.")
            if (level2Files := repackResult.getFilesAtLevel(2)) is not None:
                msg2 = QMessageBox.warning(None, "Note!", f"The following files were successfully added:\n\n{level2Files}\n\nClash has extremely similar versions of these files with the same name - shtickerpack can't tell which one you meant to change, so it added both. This is likely fine but may cause some unexpected behaviour - let me know on Github if you have any weird behaviour in-game.")
            if (level1Files := repackResult.getFilesAtLevel(1)) is not None:
                msg1 = QMessageBox.information(None, "Note!", f"The following files were successfully added:\n\n{level1Files}\n\nClash has identical versions of these files with the same name - shtickerpack can't tell which one you meant to change, so it added both. This is probably fine but may cause some unexpected behaviour - let me know on Github if you have any weird behaviour in-game.")

        
    def handleRepackResultThread(self, threadResult: "ThreadResult"): 
        threadResult.messageType(self.parentWindow, threadResult.title, threadResult.text)
    
    def repackTargetDir(self, button: QPushButton):
        deleteFiles = self.delFilesModeBox.isChecked()
        deleteFolders = self.delFoldersModeBox.isChecked()
        outputDir = None
        sourceDir = self.inputDirPath.text()
        modName = self.modNameEntry.text()
        if modName.endswith(".mf"): modName = modName[:-3]

        if self.moveOutputModeBox.isChecked():
            outputDir = self.DEFAULT_OUTPUT_DIR 
            if engine.modExists(outputDir, modName):
                msg = QMessageBox.critical(None, "Mod already exists!", f"{modName}.mf already exists in the output folder!\n({outputDir})")
                return False
        else: 
            if engine.modExists(sourceDir, modName):
                msg = QMessageBox.critical(None, "Mod already exists!", f"{modName}.mf already exists in the output folder!\n({sourceDir})")
                return False
        if not modName.isalnum(): #should refactor these checks but w/e...
            msg = QMessageBox.critical(None, "Invalid mod name!", "Your mod name can only be alphanumeric! Note your mod name shouldn't end with '.mf'.")
            return False
       
        if engine.modExists(self.DEFAULT_OUTPUT_DIR, modName):
            msg = QMessageBox.critical(None, "Mod already exists!", f"{modName}.mf already exists in the output folder!\n({outputDir})")
            return False
        #no pre-pack errors, we are good to go
        button.setText("Repacking... just a sec!")
        print("Beginning repack...")
        button.setEnabled(False)
        #incantations to run unpacker as a separate thread, via UnpackWorker()
        self.thread = QThread()
        self.worker = RepackWorker(dir=sourceDir, outputDir=outputDir, modName=modName, deleteFiles=deleteFiles, deleteFolders=deleteFolders)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.thread.finished.connect(self.worker.deleteLater)
        self.worker.result.connect(self.handleRepackResultData)
        self.worker.finished.connect(self.handleRepackResultThread)
        self.thread.start()

        self.thread.finished.connect(
            lambda: button.setEnabled(True)
        )
        self.thread.finished.connect(
            lambda: button.setText("Go!")
        )

class QHorizontalSpacer(QFrame):
    def __init__(self):
        super(QHorizontalSpacer, self).__init__()
        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)

class ThreadResult():
    def __init__(self, ok: bool, style: QMessageBox = None, title: str = None, text: str = None):
        self.ok = ok
        self.messageType = style
        self.title = title
        self.text = text

class RepackWorker(QObject):
    result = pyqtSignal(engine.phasePackOverallResult) 
    finished = pyqtSignal(ThreadResult)
    #progress = pyqtSignal(int)

    def __init__(self, dir, outputDir, modName, deleteFiles, deleteFolders):
        super(RepackWorker, self).__init__()
        self.dir = dir
        self.outputDir = outputDir
        self.modName = modName
        self.deleteFiles = deleteFiles
        self.deleteFolders = deleteFolders

    def run(self):
        """Launch the unpacking process."""
        #debugpy.debug_this_thread() #must be done to enable debugging!!!
        try:
            data: engine.phasePackOverallResult = engine.repackAllLooseFiles(
                cwd=self.dir, 
                output_dir=self.outputDir, 
                output_name=self.modName, 
                delete_file_mode=self.deleteFiles, 
                delete_folder_mode=self.deleteFolders)    
        except CalledProcessError as e:
            self.finished.emit(ThreadResult(False, QMessageBox.critical, "Warning!",
                f"Multify error! Please let me know ASAP on GitHub.\nError text:\n{e}"))
        except FileNotFoundError as e:
            self.finished.emit(ThreadResult(False, QMessageBox.critical, "Warning!",
                f"Lookup table error! Please let me know ASAP on Github.\nError text:\n{e}\nCWD:\n{os.getcwd()}"))
        except Exception as e:
            self.finished.emit(ThreadResult(False, QMessageBox.critical, "Warning!",
                f"Unknown error! Please let me know ASAP on GitHub.\nError text:\n{e}"))
        else:
            if len(data.files) == 0:
                self.finished.emit(ThreadResult(True, QMessageBox.warning, "Note!",
                    f"There weren't any valid files in that folder!"))
            else:
                self.finished.emit(ThreadResult(True, QMessageBox.information, "Success!",
                    f"{len(data.files)} files successfully packed!"))
            self.result.emit(data)

class UnpackWorker(QObject):
    success = pyqtSignal() #this is so awful.... enum>?????
    result = pyqtSignal(ThreadResult)

    def __init__(self, sourceDir, destinationDir):
        super(UnpackWorker, self).__init__()
        self.dir = dir
        self.sourceDir = sourceDir
        self.destinationDir = destinationDir

    def run(self):
        #debugpy.debug_this_thread() #must be added/removed manually to debug in thread
        try:
            engine.unpackDirectory(self.sourceDir, self.destinationDir)
        except CalledProcessError as e:
            self.result.emit(ThreadResult(False, QMessageBox.critical, "Warning!",
                f"Multify error! Please let me know ASAP on GitHub.\nError text:\n{e.__dict__}"))
        except Exception as e:
            self.result.emit(ThreadResult(False, QMessageBox.critical, "Warning!",
                f"Unknown error! Please let me know ASAP on GitHub.\nError text:\n{e.__dict__}"))
        else:
            self.result.emit(ThreadResult(True, QMessageBox.information, "Success!",
                "Folder unpacked!"))
        finally:
            self.success.emit()


if __name__ == "__main__":
    #QApplication object is the app, sys.argv are the cmd line args
    app = QApplication(sys.argv)

    app.setApplicationName(APP_NAME)
    app.setOrganizationName(ORG_NAME)
    app.setApplicationVersion(APP_VER)

    #create a widget (the window)
    window = ShtickerpackMainWindow()
    window.show() #need to explicitly show it, windows (w/o a visible parent) are hidden by default

    #start the event loop
    app.exec()

    #reaches here once app exits and event loop stops