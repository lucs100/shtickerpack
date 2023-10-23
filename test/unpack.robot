*** Settings ***
Documentation     The test suite for the shtickerpack engine.
Library    OperatingSystem
Library    Collections
Library    ./lib/engineLib.py

*** Variables ***
${ClashResources}            C:/Users/Lucas/AppData/Local/Corporate Clash/resources/contentpacks
${LooseFileWorkspace}        C:/Users/Lucas/Documents/projects/Python/shtickerpack/sandbox/loose_files
${LooseFilesClean}           C:/Users/Lucas/Documents/projects/Python/shtickerpack/sandbox/temp_good_files
${LooseFilesDuplicate}       C:/Users/Lucas/Documents/projects/Python/shtickerpack/sandbox/temp_dupe_files
${LooseFilesCleanAndDuplicate}     C:/Users/Lucas/Documents/projects/Python/shtickerpack/sandbox/temp_good_and_dupe_files
${UnpackInput}        C:/Users/Lucas/Documents/projects/Python/shtickerpack/sandbox/example_files
${UnpackOutput}       C:/Users/Lucas/Documents/projects/Python/shtickerpack/sandbox/example_output
${EmptyPhaseCount}        0
${ExpectedPhaseCount}     14
${True}     True
${False}    False

*** Test Cases ***
Unpack Default Files
    [Tags]    unpack     default assets
    Empty Directory      ${UnpackOutput}
    ${PhaseCount} =     Count Directories In Directory    ${UnpackOutput}
    Should Be Equal As Integers     ${PhaseCount}     ${EmptyPhaseCount}
    Unpack All Files
    Count Directories In Directory    ${UnpackOutput}
    ${PhaseCount} =     Count Directories In Directory    ${UnpackOutput}
    Should Be Equal As Integers     ${PhaseCount}     ${ExpectedPhaseCount}

    
*** Keywords ***
    