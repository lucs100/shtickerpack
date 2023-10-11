import os, re, shutil, time, subprocess, json, pathlib

CWD_PATH = os.path.dirname(__file__)
MULTIFY_PATH = os.path.join(CWD_PATH, "panda3d", "multify.exe")
#might want to remove on release? not helpful
DEFAULT_TARGET_FILE_PATH = os.path.join(CWD_PATH, "test", "example_files")
DEFAULT_DESTINATION_PATH = os.path.join(CWD_PATH, "test", "example_output")
PHASE_LUT = {}

class TTScaryFileException(Exception):
    def __init__(self, message):
        super.__init__(message)

def _isTargetFile(fp: str) -> bool:
    """
    Returns whether the target file is a phase file that can be unlocked and edited via a regex.
    Allows for capture of phase file name.
    """
    return re.search("^phase_[\d\.]+_(?!models|dna|paths|luts|shaders).*$", fp)

def _isMultiFile(fp: str) -> bool:
    """
    Returns whether the target file is a .mf file via a regex.
    Allows for capture of phase file name.
    """
    return re.search("^(.*)\.mf$", fp)

def _isPhaseDir(dp: str) -> bool:
    """
    Returns whether the target directory is a phase file directory via a regex.
    Allows for capture of phase file name.
    """
    return re.search("^(phase_\d\.?\d?)$", dp)

def _unpackFile(dir: str, filename: str, target_dir: str=CWD_PATH):
    """
    Uses the multify tool to unpack a Panda3D multifile.
    By default, leaves phase_X folders in the current directory. Optional target_dir changes this behaviour.
    """
    start = time.time()
    subprocess.run(f"{MULTIFY_PATH} -x -f \"{dir}/{filename}\"", shell=True, cwd=target_dir)
    end = time.time()    
    print(f"Unpacked {filename}! \t took {round(end-start, 2)}s")

def unpackDirectory(target_dir: str = DEFAULT_TARGET_FILE_PATH, output_dir: str=CWD_PATH, strict_mode: bool = True) -> bool:
    """
    Uses the multify tool to unpack all Panda3D multifiles in a directory.
    By default, leaves output folders in the current directory. destination_dir changes this behaviour.
    strict_mode matches only phase_x.mf, otherwise, matches any phase files.
    """
    fileList: list = os.listdir(target_dir)
    if strict_mode: targetFileList = filter(_isTargetFile, fileList)
    else:           targetFileList = filter(_isMultiFile, fileList)
    for file in targetFileList:
        _unpackFile(target_dir, file, output_dir)
    return True

def _checkTargetUnphased(targetDir: str) -> bool:
    """
    Ensures that phase directories will not get overwritten.
    If any phase_X folders exist in targetDir, returns False (error). Otherwise, returns true.
    """
    objsInDir = os.listdir(targetDir)
    for obj in objsInDir:
        if _isPhaseDir(obj):
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
    targetMoveList = filter(_isPhaseDir, folderList)
    
    if checkOutputDirectoryValid(toPath):
        for dir in targetMoveList:
            print(f"Moving: {str.rjust('/'+dir+'/', 12)} to /{toPath}/ ...", end="")
            shutil.move(dir, toPath)
            print(" done.")
    else: print("Aborting to avoid overwrite...")

def spaceDelimit(file_list: list, base_dir: str="") -> str:
    """Convenience method to turn a list into a space-separated string."""
    if isinstance(file_list, filter):
        file_list = list(file_list)
    targetMoveStr = "" 
    for file in file_list:
        targetMoveStr += (f"{base_dir}/{file} ") #multify repack argument must be space-separated dir names
    return targetMoveStr

def repackList(cwd: str = DEFAULT_TARGET_FILE_PATH, file_list: str = "", output_name: str = "defaultPackName", output_dir: str = None):
    """
    Manually repacks all folders specified in the file_list parameter. Can be str or simple iterable.
    """
    if output_dir == None: output_dir = cwd
    if not isinstance(file_list, str): #assume iterable 
        file_list = spaceDelimit(file_list, base_dir=cwd)
    if file_list == "": return # no files passed
    
    prepDir(output_dir)
    
    print(f"Beginning repack! This will take a few seconds if you didn't purge existing assets...")
    start = time.time()
    subprocess.run(f"{MULTIFY_PATH} -c -f {output_name}.mf {file_list}", shell=True, cwd=output_dir)
    end = time.time()
    print(f"Repacked {output_name}.mf! \t took {round(end-start, 2)}s")

def repackAllInDirectory(target_dir: str = DEFAULT_TARGET_FILE_PATH, output_name: str = "defaultPackName", output_dir: str = None) -> None:
    """
    Repacks all phase_X folders in the target directory into a single multifile named output_name.mf.
    Optionally, creates this file in destination_dir.
    """
    folderList = os.listdir(target_dir)
    targetMoveList = list(filter(_isPhaseDir, folderList))
    repackList(cwd=target_dir, file_list=targetMoveList, output_name=output_name, output_dir=output_dir)

def prepDir(dir_name: str) -> bool:
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
        return True
    return False

def loadLUT(fp: str) -> dict:
    with open(fp, 'r') as file:
        return json.loads(file.read())

def moveFileToPhaseStructure(filename: str, cwd: str):
    """
    Accepts one file filename in the directory cwd. If it exists in the file LUT, moves it to the
    expected phase path, creating the files where neccesary. Returns the top-level destination names.
    """
    global PHASE_LUT
    cwd = pathlib.Path(cwd)
    errorFiles = {1:[], 2:[], 3:[]}
    if filename in PHASE_LUT:

        filepaths = PHASE_LUT[filename]['fp']
        fileWarningLevel = PHASE_LUT[filename]['warning_level']

        if fileWarningLevel in [0, 1, 2]:
            for path in filepaths:
                tgtPath = cwd / pathlib.Path(path)
                if not tgtPath.exists():
                    tgtPath.mkdir(parents=True)
                fromPath = cwd / filename
                shutil.move(str(fromPath), str(tgtPath))
            if fileWarningLevel > 0:
                errorFiles[fileWarningLevel].append(filename)
        elif fileWarningLevel == 3:
            raise TTScaryFileException(f"{filename} is a level 3 file, which are not implemented yet.")
            #case-by-case, sadly
        
        return [pathlib.Path(fp).parts[0] for fp in filepaths] #all phase_x folders

def repackAllLooseFiles(cwd: str, output_dir = DEFAULT_DESTINATION_PATH, output_name = "defaultPackName", strictMode: bool = True):
    """
    Moves all loose files in a directory cwd to their expected phase paths, 
    creating them where neccesary. If targetDir is passed, moves the resulting file to that directory.
    strictMode moves only altered phase folders. outputName sets the output .mf filename (defaults to in-place).
    """
    #TODO: recursive mode
    changedDirs = set()
    for item in pathlib.Path(cwd).iterdir():
        if item.is_file():
            newDirs = moveFileToPhaseStructure(item.name, cwd)
            changedDirs.update(newDirs)
    if strictMode:  repackList(cwd=cwd, file_list=changedDirs, output_dir=output_dir, output_name=output_name)
    else:           repackAllInDirectory(cwd=cwd, output_dir=output_dir, output_name=output_name)   


if __name__ == "__main__":
    #used for testing
    # unpackDirectory(target_dir="C:/Users/Lucas/Documents/projects/Python/shtickerpack/test/example_files", output_dir="C:/Users/Lucas/Documents/projects/Python/shtickerpack/test/example_output")
    # movePhaseToDirectory()
    repackAllInDirectory(target_dir="C:/Users/Lucas/Documents/projects/Python/shtickerpack/test/example_output", output_dir="C:/Users/Lucas/Documents/projects/Python/shtickerpack/test/newTestFolder")
    
    # PHASE_LUT = loadLUT("./lut/file_lut.json")
    # targetDir = "C:/Users/Lucas/Documents/projects/Python/shtickerpack/test/loose_files"
    # repackAllLooseFiles(cwd=targetDir, 
    #     output_dir="C:/Users/Lucas/Documents/projects/Python/shtickerpack/test/loose_files_packed",
    #     output_name="loosePackTest")
