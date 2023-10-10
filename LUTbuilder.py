import pathlib, filecmp, typing

path = "C:/Users/Lucas/Documents/projects/Python/shtickerpack/test/example_output"

phase = pathlib.Path(path)

#yeah, manual unfortunately.
LEVEL_1_LIST = ["clock03.ogg", "grass.png", "shirt_Sleeve_pumkin.png", "tt_t_chr_avt_acc_sho_athleticGreen.png", "tt_t_chr_avt_acc_sho_docMartinBootsGreen.png", "tt_t_chr_avt_acc_sho_docMartinBootsGreenLL.png"]
LEVEL_2_LIST = ["AA_drop_anvil_miss.ogg", "avatar_emotion_taunt.ogg", "MG_win.ogg", "toontown_central_common_palette_4amla_1.png", "tt_t_chr_avt_skirt_halloween2.png", "Golf_Crowd_Miss.ogg", "stripeB5.png"]
LEVEL_3_LIST = ["cog.png", "box_side1.png", "stripeB2.png", "stripeB4.png"]

class LUTFile:
    def __init__(self, file: pathlib.Path):
        if file.is_file():
            self.name = file.name
            self.path = file.parent
            self.warningLevel = 0
            #0 = unique file, standard case
            #1 = identical file used elsewhere - replace both
            #2 = similar file used elsewhere, one is likely outdated - replace both
            #3 = different file used elsewhere, need to identify case-by-case
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
            fileA.warningLevel = 1
            fileB.warningLevel = 1
        else:
            print(f"Non-equal duplicate found.\t{fileA.name}\n{fileA}\n{fileB}\nBad :( ")
            if fileA.name in LEVEL_1_LIST:
                fileA.warningLevel = 1
                fileB.warningLevel = 1
            elif fileA.name in LEVEL_2_LIST:
                fileA.warningLevel = 2
                fileB.warningLevel = 2
            elif fileB.name in LEVEL_3_LIST:
                fileA.warningLevel = 3
                fileB.warningLevel = 3
            else:
                print("Uncaught file! Exiting.")
                exit()
        file = fileB
    fileList.append(file)
    #print(f"Added {file}! Length: {len(fileList)}")

def recursiveAddFiles(pathItem: pathlib.Path):
    for item in pathItem.iterdir():
        if item.is_dir():
            recursiveAddFiles(item)
        if item.is_file():
            conditionalAppend(LUTFile(item))

recursiveAddFiles(phase)