import os, sys, time
from time import sleep
import threading
import pygetwindow
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt

rootpath = os.path.abspath(f"C:/Users/Lucas/Documents/projects/Python/shtickerpack/src") #manual, unfortunately
sys.path.append(rootpath)
os.chdir(rootpath)

DEFAULT_LOOSE_FILES_DIR = f"C:/Users/Lucas/Documents/projects/Python/shtickerpack/sandbox/loose_files" #could make generic... ehh
DEFAULT_CONTENTPACKS_DIR = f"C:/Users/{os.getlogin()}/AppData/Local/Corporate Clash/resources/contentpacks"
DEFAULT_PHASE_INPUT_DIR = f"C:/Users/{os.getlogin()}/AppData/Local/Corporate Clash/resources/default"
DEFAULT_PHASE_OUTPUT_DIR =f"C:/Users/Lucas/Documents/projects/Python/shtickerpack/sandbox/example_output" #sorry contributors :( help appreciated

import client, engine

app = QApplication(sys.argv)

app.setApplicationName(client.APP_NAME)
app.setOrganizationName(client.ORG_NAME)
app.setApplicationVersion(client.APP_VER)

class clientGUILib():
    #ROBOT_LIBRARY_VERSION = __version__
    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self):
        self.gui = client.ShtickerpackMainWindow() 
        self.gui.show()
        self.repackPanel = self.gui.repackFilePanel
        self.TITLE = self.gui.windowTitle()

    def select_tab(self, tab: int):
        self.gui.tabs.setCurrentIndex(tab)
    
    def set_repack_input(self, fp: str):
        self.repackPanel.inputDirPath.setText(fp)
        QApplication.processEvents()

    def set_repack_output_name(self, name: str):
        self.repackPanel.modNameEntry.setText(name)
        QApplication.processEvents()
    
    def set_repack_deletion_mode(self, deleteFiles: bool, deleteFolders: bool):
        self.repackPanel.delFilesModeBox.setChecked(deleteFiles)
        self.repackPanel.delFoldersModeBox.setChecked(deleteFolders)
        QApplication.processEvents()
        
    def close_active_modals(self):
        """Must be scheduled with a delay before the window is called."""
        print("Firing....")
        while isinstance(QApplication.activeWindow(), QMessageBox):
            win: QMessageBox = QApplication.activeWindow()
            closeBtn = win.defaultButton()
            QTest.mouseClick(closeBtn, Qt.MouseButton.LeftButton)
            print("Fired!")
            del win
            time.sleep(1)
            QApplication.processEvents()
    
    def verify_no_modals(self):
        assert not isinstance(QApplication.activeWindow(), QMessageBox), "A modal is still open."
        QApplication.processEvents()

    def start_gui_repack(self, delay_time=1):
        print("Queueing...")
        threading.Timer(delay_time, self.close_active_modals).start()
        QTest.mouseClick(self.repackPanel.repackButton, Qt.MouseButton.LeftButton)
        QApplication.processEvents()

if __name__ == "__main__":
    try: os.remove("C:\\Users\\Lucas\\AppData\\Local\\Corporate Clash\\resources\\contentpacks\\UITestMod.mf")
    except: pass
    app.setApplicationName(client.APP_NAME)
    app.setOrganizationName(client.ORG_NAME)
    app.setApplicationVersion(client.APP_VER)
    
    test = clientGUILib()
    test.select_tab(1)
    test.set_repack_input("C:\\Users\\Lucas\\Documents\\projects\\Python\\shtickerpack\\sandbox\\loose_files")
    test.set_repack_output_name("UITestMod")
    test.set_repack_deletion_mode(deleteFiles=False, deleteFolders=True)
    test.start_gui_repack()
    input("Continue?")

    # test = clientGUILib()
    # test.create_msg_box()
    # test.close_active_modal()