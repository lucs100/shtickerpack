import os, re, shutil, time, subprocess

CWD_PATH = os.path.dirname(__file__)
MULTIFY_PATH = os.path.join(CWD_PATH, "panda3d", "multify.exe")
DEFAULT_TARGET_FILE_PATH = os.path.join(CWD_PATH, "test", "example_files")
DEFAULT_DESTINATION_PATH = os.path.join(CWD_PATH, "test", "example_output")

def _isTargetFile(fp: str) -> bool:
    """
    Returns whether the target file is a phase file that can be unlocked and edited via a regex.
    Allows for capture of phase file name.
    """
    return re.search("(phase_[\d\.]+_(?!models|dna|paths|luts|shaders).*)\.mf", fp)

def _isTargetDir(dp: str) -> bool:
    """
    Returns whether the target directory is a phase file directory via a regex.
    Allows for capture of phase file name.
    """
    return re.search("^(phase_\d\.?\d?)$", dp)

def _multify_file(dir: str, filename: str, target_dir: str=CWD_PATH):
    """
    Uses the multify tool to unpack a Panda3D multifile.
    By default, leaves phase_X folders in the current directory. target_dir changes this behaviour.
    """
    start = time.time()
    subprocess.run([MULTIFY_PATH, "-x", "-f", os.path.join(dir, filename)], shell=True, cwd=target_dir)
    end = time.time()    
    print(f"Unpacked {filename}! \t took {round(end-start, 2)}s")

def unpackDirectory(dir: str = DEFAULT_TARGET_FILE_PATH, target_dir: str=CWD_PATH) -> None:
    """
    Uses the multify tool to unpack all Panda3D multifiles in a directory.
    By default, leaves phase_X folders in the current directory. target_dir changes this behaviour.
    """
    fileList: list = os.listdir(dir)
    targetFileList = filter(_isTargetFile, fileList)
    for file in targetFileList:
        _multify_file(dir, file, target_dir)

def _checkTargetEmpty(targetDir) -> bool:
    """
    Ensures that phase directories will not get overwritten.
    """
    objsInDir = os.listdir(targetDir)
    for obj in objsInDir:
        if _isTargetDir(obj):
            print(f"Warning: {obj} was detected as a possible existing phase file!")
            return False
    return True

def movePhaseToDirectory(fromPath=CWD_PATH, toPath=DEFAULT_DESTINATION_PATH) -> None:
    folderList = os.listdir(fromPath)
    targetMoveList = filter(_isTargetDir, folderList)
    
    if _checkTargetEmpty(toPath):
        for dir in targetMoveList:
            print(f"Moving: {str.rjust('/'+dir+'/', 12)} to /{toPath}/ ...", end="")
            shutil.move(dir, toPath)
            print(" done.")
    else: print("Aborting to avoid overwrite...")

#unpackDirectory()
#movePhaseToDirectory()

#TODO: re-multify function