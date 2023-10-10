import pathlib, filecmp, typing

path = "C:/Users/Lucas/Documents/projects/Python/shtickerpack/test/example_output"

phase = pathlib.Path(path)

class LUTFile:
    def __init__(self, file: pathlib.Path):
        if file.is_file():
            self.name = file.name
            self.path = file.parent
        else:
            self = None
    
    def fullPath(self):
        return f"{self.path}/{self.name}"
    
    def __repr__(self) -> str:
        return self.fullPath()

fileList: "list[LUTFile]" = []

def filenameInList(query: LUTFile) -> typing.Union[bool, "list[LUTFile]"]:
    queryName = query.name
    global fileList
    for file in fileList:
        if file.name == queryName:
            return [file, query]
    return False

def checkFilesEqual(fileA: LUTFile, fileB: LUTFile):
    return filecmp.cmp(fileA.fullPath(), fileB.fullPath())

def conditionalAppend(file: LUTFile):
    global fileList
    if result := filenameInList(file):
        fileA, fileB = result
        if checkFilesEqual(fileA, fileB):
            print(f"Equal duplicate found!\n{fileA}\n{fileB}\n")
        else:
            print(f"Non-equal duplicate found.\t{fileA.name}\n{fileA}\n{fileB}\nBad :( ")
    fileList.append(file)
    #print(f"Added {file}! Length: {len(fileList)}")

def recursiveAddFiles(pathItem: pathlib.Path):
    for item in pathItem.iterdir():
        if item.is_dir():
            recursiveAddFiles(item)
        if item.is_file():
            conditionalAppend(LUTFile(item))

recursiveAddFiles(phase)