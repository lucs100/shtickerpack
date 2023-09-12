import os, re, shutil, time

ABS_PATH = os.path.dirname(__file__)
MULTIFY_PATH = os.path.join(ABS_PATH, "panda3d", "multify.exe")
TARGET_FILE_PATH = os.path.join(ABS_PATH, "test", "example_files")
DESTINATION_PATH = os.path.join(ABS_PATH, "test", "example_output")

def isTargetFile(fp: str) -> bool:
    """
    Returns whether the target file is a phase file that can be unlocked and edited via a regex.
    Allows for capture of phase file name.
    """
    return re.search("(phase_[\d\.]+_(?!models|dna|paths|luts|shaders).*)\.mf", fp)

def isTargetDir(dp: str) -> bool:
    """
    Returns whether the target directory is a phase file directory via a regex.
    Allows for capture of phase file name.
    """
    return re.search("^(phase_\d\.?\d?)$", dp)

fileList: list = os.listdir(TARGET_FILE_PATH)
targetFileList = filter(isTargetFile, fileList)

def multify(filename: str):
    """
    Uses the multify tool to unpack a Panda3D multifile.
    """
    start = time.time()
    os.system(f"{MULTIFY_PATH} -x -f {os.path.join(TARGET_FILE_PATH, filename)}")
    end = time.time()    
    print(f"Multified {filename}! \t took {round(end-start, 2)}s")

for file in targetFileList:
    #multify(file)
    pass

folderList = os.listdir(ABS_PATH)
targetMoveList = filter(isTargetDir, folderList)

def checkTargetEmpty(targetDir) -> bool:
    """
    Ensures that phase directories will not get overwritten.
    """
    objsInDir = os.listdir(targetDir)
    for obj in objsInDir:
        if isTargetDir(obj):
            print(f"{obj} was detected as a possible existing phase file! Exiting to avoid overwrite...")
            exit()
    return True

ok = checkTargetEmpty(DESTINATION_PATH)

for dir in targetMoveList:
    print(f"Moving: {str.rjust('/'+dir+'/', 12)} to /{DESTINATION_PATH}/ ...", end="")
    shutil.move(dir, DESTINATION_PATH)
    print(" done.")