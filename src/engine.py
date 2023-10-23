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
        if base_dir == "":  targetMoveStr += (f"{file} ") #multify repack argument must be space-separated dir names
        else:               targetMoveStr += (f"{base_dir}/{file} ") 
    return targetMoveStr.strip()

def _repackList(cwd: str = DEFAULT_TARGET_FILE_PATH, folder_list: str = "", output_name: str = "defaultPackName", output_dir: str = None, delete_mode: bool = False):
    """
    Manually repacks all folders specified in the file_list parameter. Can be str or simple iterable.
    Moves the output file to output_dir if specified (leaves in-place by default).
    """
    if not isinstance(folder_list, str): #assume iterable 
        file_list_str = spaceDelimit(folder_list) #no base_dir, as we're in the right cwd
    if file_list_str == "": return # no files passed
    
    if output_dir != None: prepDir(output_dir)
    
    print(f"Beginning repack! This may take a few seconds...")
    start = time.time()
    subprocess.run(f"{MULTIFY_PATH} -c -f {output_name}.mf {file_list_str}", shell=True, cwd=cwd)
    end = time.time()
    print(f"Repacked {output_name}.mf! \t took {round(end-start, 2)}s")
    if output_dir != None:
        shutil.move(f"{cwd}/{output_name}.mf", output_dir)
    if delete_mode:
        for folder in folder_list:
            try: shutil.rmtree(f"{cwd}/{folder}")
            except FileNotFoundError: print(f"Skipping deletion of {cwd}/{folder}... (Doesn't exist)")


def _repackAllInDirectory(target_dir: str = DEFAULT_TARGET_FILE_PATH, output_name: str = "defaultPackName", output_dir: str = None) -> None:
    """
    Repacks all phase_X folders in the target directory into a single multifile named output_name.mf.
    Optionally, creates this file in destination_dir.
    """
    folderList = os.listdir(target_dir)
    targetMoveList = list(filter(_isPhaseDir, folderList))
    _repackList(cwd=target_dir, folder_list=targetMoveList, output_name=output_name, output_dir=output_dir)

def prepDir(dir_name: str) -> bool:
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
        return True
    return False

def loadLUT(fp: str) -> dict:
    with open(fp, 'r') as file:
        return json.loads(file.read())

class phasePackResult:
    def __init__(self, folders: list = None, file: str = None, warnings: "dict[str: int]" = None):
        self.folders: list = folders or list()
        self.file: str = file or str()
        self.warnings: "dict[str: int]" = warnings or dict()

    def isClean(self) -> bool:
        return (self.warnings == {})

class phasePackOverallResult:
    def __init__(self, folders: set = None, files: list = None, warnings: "dict[str: int]" = None):
        self.folders: set = folders or set()
        self.files: list = files or list()
        self.warnings: "dict[str: int]" = warnings or dict()
    
    def isClean(self) -> bool:
        return (self.warnings == {})
    
    def addResult(self, result: phasePackResult):
        if result is None: return #file is not a phase file, should warn somehow... oh well #TODO
        self.folders.update(result.folders)
        self.files.append(result.file)
        self.warnings.update(result.warnings)

    def getFilesAtLevel(self, queryLevel: int) -> "list[str]":
        output = []
        for file, level in self.warnings.items():
            if level == queryLevel:
                output.append(file)
        if output == []: return None
        else: return output

def moveFileToPhaseStructure(filename: str, cwd: str, delete_mode: bool = False) -> phasePackResult:
    """
    Accepts one file filename in the directory cwd. If it exists in the file LUT, moves it to the
    expected phase path, creating the files where neccesary. Returns the top-level destination names.
    """
    global PHASE_LUT
    cwd = pathlib.Path(cwd)
    result = phasePackResult()
    if filename in PHASE_LUT:

        filepaths = PHASE_LUT[filename]['fp']
        fileWarningLevel = PHASE_LUT[filename]['warning_level']
        result.file = filename

        if fileWarningLevel in [0, 1, 2]:
            moved = False
            for path in filepaths:
                tgtPath = cwd / pathlib.Path(path)
                if not tgtPath.exists():
                    tgtPath.mkdir(parents=True)
                fromPath = cwd / filename
                shutil.copy(str(fromPath), str(tgtPath))
                moved = True
            if moved and delete_mode: os.remove(str(fromPath)) #DONT del unmoved files
        if fileWarningLevel > 0:
            result.warnings[filename] = fileWarningLevel
        #elif fileWarningLevel == 3:
            #raise TTScaryFileException(f"{filename} is a level 3 file, which are not implemented yet.")
            #case-by-case, sadly
            #TODO: level 3 logic
        
        result.folders = [pathlib.Path(fp).parts[0] for fp in filepaths] #all phase_x folders
        return result
    else:
        result.warnings[filename] = 4 #not found in lut

def repackAllLooseFiles(cwd: str, output_dir = None, output_name = "defaultPackName", 
    strictMode: bool = True, delete_file_mode: bool = False, delete_folder_mode: bool = False):
    """
    Moves all loose files in a directory cwd to their expected phase paths, 
    creating them where neccesary. If output_dir is passed, moves the resulting file to that directory.
    strictMode moves only altered phase folders. outputName sets the output .mf filename (defaults to in-place).
    delete_file_mode deletes loose copies of files when done.
    delete_folder_mode deletes phase_x folders when done.
    """
    #TODO: recursive mode
    global PHASE_LUT
    if PHASE_LUT == {}: PHASE_LUT = loadLUT("./lut/file_lut.json")
    overallResult = phasePackOverallResult()
    for item in pathlib.Path(cwd).iterdir():
        if item.is_file():
            result = moveFileToPhaseStructure(item.name, cwd, delete_mode=delete_file_mode)
            if 4 not in result.warnings.values(): #4 = not in lut
                overallResult.addResult(result)
            if not result.isClean():
                for file, level in result.warnings.items():
                    print(f"Level {level} warning: {file}") 
    if strictMode:  _repackList(cwd=cwd, folder_list=overallResult.folders, output_dir=output_dir, output_name=output_name, delete_mode=delete_folder_mode)
    else:           _repackAllInDirectory(cwd=cwd, output_dir=output_dir, output_name=output_name, delete_mode=delete_folder_mode)
    return overallResult

def modExists(outputDir: str, modName: str) -> bool:
    return pathlib.Path(f"{outputDir}/{modName}.mf").exists()



if __name__ == "__main__":
    #used for testing
    # unpackDirectory(target_dir="C:/Users/Lucas/Documents/projects/Python/shtickerpack/sandbox/example_files", output_dir="C:/Users/Lucas/Documents/projects/Python/shtickerpack/sandbox/example_output")
    # movePhaseToDirectory()
    # repackAllInDirectory(target_dir="C:/Users/Lucas/Documents/projects/Python/shtickerpack/sandbox/example_output")
    
    # PHASE_LUT = loadLUT("./lut/file_lut.json")
    # targetDir = "C:/Users/Lucas/Documents/projects/Python/shtickerpack/sandbox/loose_files"
    # repackAllLooseFiles(cwd=targetDir, output_name="loosePackTest")
    pass
