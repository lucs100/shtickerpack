import os, re, shutil, time, subprocess

CWD_PATH = os.path.dirname(__file__)
MULTIFY_PATH = os.path.join(CWD_PATH, "panda3d", "multify.exe")
#might want to remove on release? not helpful
DEFAULT_TARGET_FILE_PATH = os.path.join(CWD_PATH, "test", "example_files")
DEFAULT_DESTINATION_PATH = os.path.join(CWD_PATH, "test", "example_output")

def _isTargetFile(fp: str) -> bool:
    """
    Returns whether the target file is a phase file that can be unlocked and edited via a regex.
    Allows for capture of phase file name.
    """
    return re.search("^phase_[\d\.]+_(?!models|dna|paths|luts|shaders).*$", fp)

def _isTargetDir(dp: str) -> bool:
    """
    Returns whether the target directory is a phase file directory via a regex.
    Allows for capture of phase file name.
    """
    return re.search("^(phase_\d\.?\d?)$", dp)

def _multifyFile(dir: str, filename: str, target_dir: str=CWD_PATH):
    """
    Uses the multify tool to unpack a Panda3D multifile.
    By default, leaves phase_X folders in the current directory. Optional target_dir changes this behaviour.
    """
    start = time.time()
    subprocess.run(f"{MULTIFY_PATH} -x -f \"{dir}/{filename}\"", shell=True, cwd=target_dir)
    end = time.time()    
    print(f"Unpacked {filename}! \t took {round(end-start, 2)}s")

def unpackDirectory(target_dir: str = DEFAULT_TARGET_FILE_PATH, destination_dir: str=CWD_PATH) -> bool:
    """
    Uses the multify tool to unpack all Panda3D multifiles in a directory.
    By default, leaves phase_X folders in the current directory. destination_dir changes this behaviour.
    """
    fileList: list = os.listdir(target_dir)
    targetFileList = filter(_isTargetFile, fileList)
    for file in targetFileList:
        _multifyFile(target_dir, file, destination_dir)
    return True

def _checkTargetUnphased(targetDir: str) -> bool:
    """
    Ensures that phase directories will not get overwritten.
    If any phase_X folders exist in targetDir, returns False (error). Otherwise, returns true.
    """
    objsInDir = os.listdir(targetDir)
    for obj in objsInDir:
        if _isTargetDir(obj):
            print(f"Warning: {obj} was detected as a possible existing phase file!")
            #TODO: raise PhaseExistsException(f"warning...")?
            return False
    return True

def checkOutputDirectoryValid(targetDir: str) -> bool:
    """
    Ensures the output folder targetDir exists AND has no phase folders in it. 
    """
    return os.path.exists(targetDir) and _checkTargetUnphased(targetDir)

def movePhaseToDirectory(fromPath=CWD_PATH, toPath=DEFAULT_DESTINATION_PATH) -> None:
    """
    Moves all phase_X folders found in directory fromPath to the directory toPath.
    Convenience function, use unpackDirectory() with parameter target_dir for less mess where possible
    """
    folderList = os.listdir(fromPath)
    targetMoveList = filter(_isTargetDir, folderList)
    
    if checkOutputDirectoryValid(toPath):
        for dir in targetMoveList:
            print(f"Moving: {str.rjust('/'+dir+'/', 12)} to /{toPath}/ ...", end="")
            shutil.move(dir, toPath)
            print(" done.")
    else: print("Aborting to avoid overwrite...")

def repackDirectory(target_dir: str = DEFAULT_TARGET_FILE_PATH, output_name: str = "soplePack", destination_dir: str = None) -> None:
    """
    Repacks all phase_X folders in the target directory into a single multifile named output_name.mf.
    Optionally, creates this file in destination_dir.
    """
    if destination_dir == None: destination_dir = target_dir
    folderList = os.listdir(target_dir)
    targetMoveList = filter(_isTargetDir, folderList)
    targetMoveStr = "" 
    for file in targetMoveList:
        targetMoveStr += (f"{target_dir}/{file} ") #multify repack argument must be space-separated dir names
    
    print(f"Beginning repack! This will take a few seconds if you didn't purge existing assets...")
    start = time.time()
    subprocess.run(f"{MULTIFY_PATH} -c -f {output_name}.mf {targetMoveStr}", shell=True, cwd=destination_dir)
    end = time.time()
    print(f"Repacked {output_name}.mf! \t took {round(end-start, 2)}s")

def prepVanilla(vanilla_dir: str) -> bool:
    if not os.path.exists(vanilla_dir):
        os.mkdir(vanilla_dir)
        return True
    return False

if __name__ == "__main__":
    unpackDirectory()
    movePhaseToDirectory()
    repackDirectory("C:/Users/Lucas/Documents/projects/Python/shtickerpack/test/example_output", 
        destination_dir="C:/Users/Lucas/Documents/projects/Python/shtickerpack/test/newTestFolder")