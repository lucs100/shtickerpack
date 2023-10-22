import os
import sys

rootpath = os.path.abspath(f"C:/Users/{os.getlogin()}/Documents/projects/Python/shtickerpack")
sys.path.append(rootpath)

import engine

DEFAULT_LOOSE_FILES_DIR = f"C:/Users/{os.getlogin()}/Documents/projects/Python/shtickerpack/sandbox/loose_files"
DEFAULT_CONTENTPACKS_DIR = f"C:/Users/{os.getlogin()}/AppData/Local/Corporate Clash/resources/contentpacks"

class engineLib(object):
    #ROBOT_LIBRARY_VERSION = __version__
    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self):
        pass

    def repack_loose_files(self, sourceDir=DEFAULT_LOOSE_FILES_DIR, output_name="_TEST", deleteFiles=False, deleteFolders=False):
        engine.repackAllLooseFiles(cwd=sourceDir, output_name=output_name, output_dir=DEFAULT_CONTENTPACKS_DIR,
            delete_file_mode=deleteFiles, delete_folder_mode=deleteFolders)

if __name__ == "__main__":
    test = engineLib()
    test.repack_loose_files(deleteFolders=True)