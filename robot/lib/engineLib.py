import os
import sys

rootpath = os.path.abspath(f"C:/Users/{os.getlogin()}/Documents/projects/Python/shtickerpack")
sys.path.append(rootpath)

import engine

DEFAULT_LOOSE_FILES_DIR = f"C:/Users/{os.getlogin()}/Documents/projects/Python/shtickerpack/sandbox/loose_files"
DEFAULT_CONTENTPACKS_DIR = f"C:/Users/{os.getlogin()}/AppData/Local/Corporate Clash/resources/contentpacks"
DEFAULT_PHASE_INPUT_DIR = f"C:/Users/{os.getlogin()}/AppData/Local/Corporate Clash/resources/default"
DEFAULT_PHASE_OUTPUT_DIR =f"C:/Users/{os.getlogin()}/Documents/projects/Python/shtickerpack/sandbox/example_output"

class engineLib(object):
    #ROBOT_LIBRARY_VERSION = __version__
    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self):
        pass

    def repack_loose_files(self, sourceDir=DEFAULT_LOOSE_FILES_DIR, output_name="_TEST", deleteFiles=False, deleteFolders=False):
        engine.repackAllLooseFiles(cwd=sourceDir, output_name=output_name, output_dir=DEFAULT_CONTENTPACKS_DIR,
            delete_file_mode=deleteFiles, delete_folder_mode=deleteFolders)
    
    def unpack_all_files(self, source_dir=DEFAULT_PHASE_INPUT_DIR, output_dir=DEFAULT_PHASE_OUTPUT_DIR):
        engine.unpackDirectory(target_dir=source_dir, output_dir=output_dir)

if __name__ == "__main__":
    test = engineLib()
    test.repack_loose_files(deleteFolders=True)