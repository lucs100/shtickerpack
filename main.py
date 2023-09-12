import os, re

ABS_PATH = os.path.dirname(__file__)
MULTIFY_PATH = os.path.join(ABS_PATH, "panda3d", "multify.exe")
TARGET_FILE_PATH = os.path.join(ABS_PATH, "test", "example_files")

def isTargetFile(fp):
    #regex matching only files that can be unlocked and edited
    #overcomplicated, but i like regex and it allows for capture of mf name later
    return re.search("(phase_[\d\.]+_(?!models|dna|paths|luts|shaders).*)\.mf", fp)

fileList: list = os.listdir(TARGET_FILE_PATH)
targetFileList = list(filter(isTargetFile, fileList))

#os.system(f"{MULTIFY_PATH} -x -f {os.path.join(TARGET_FILE_PATH, fileList[0])}")