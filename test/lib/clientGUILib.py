import os, sys

from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt

rootpath = os.path.abspath(f"C:/Users/Lucas/Documents/projects/Python/shtickerpack/src") #manual, unfortunately
sys.path.append(rootpath)
os.chdir(rootpath)

DEFAULT_LOOSE_FILES_DIR = f"C:/Users/Lucas/Documents/projects/Python/shtickerpack/sandbox/loose_files" #could make generic... ehh
DEFAULT_CONTENTPACKS_DIR = f"C:/Users/{os.getlogin()}/AppData/Local/Corporate Clash/resources/contentpacks"
DEFAULT_PHASE_INPUT_DIR = f"C:/Users/{os.getlogin()}/AppData/Local/Corporate Clash/resources/default"
DEFAULT_PHASE_OUTPUT_DIR =f"C:/Users/Lucas/Documents/projects/Python/shtickerpack/sandbox/example_output" #sorry contributors :( help appreciated

import client

app = QApplication(sys.argv)

class clientGUILib(object):
    #ROBOT_LIBRARY_VERSION = __version__
    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self):
        self.gui = client.ShtickerpackMainWindow() 
        self.repackPanel = self.gui.repackFilePanel

    def select_tab(self, tab: int):
        self.gui.tabs.setCurrentIndex(tab)
    
    def set_repack_input(self, fp: str):
        self.repackPanel.inputDirPath.setText(fp)

    def set_repack_output_name(self, name: str):
        self.repackPanel.modNameEntry.setText(name)
    
    def set_repack_deletion_mode(self, deleteFiles: bool, deleteFolders: bool):
        self.repackPanel.delFilesModeBox.setChecked(deleteFiles)
        self.repackPanel.delFoldersModeBox.setChecked(deleteFolders)
    
    def start_repack(self):
        QTest.mouseClick(self.repackPanel.repackButton, Qt.MouseButton.LeftButton)


if __name__ == "__main__":
    test = clientGUILib()
    test.select_tab(1)
    test.set_repack_input("C:\\Users\\Lucas\\Documents\\projects\\Python\\shtickerpack\\sandbox\\loose_files")
    test.set_repack_output_name("UITestMod")
    test.set_repack_deletion_mode(deleteFiles=False, deleteFolders=True)
    test.start_repack()
    input()
    