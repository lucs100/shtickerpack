*** Settings ***
Documentation     The test suite for the shtickerpack engine.
Library    OperatingSystem

*** Variables ***
${ClashResources}            C:/Users/Lucas/AppData/Local/Corporate Clash/resources/contentpacks
${LooseFileWorkspace}        C:/Users/Lucas/Documents/projects/Python/shtickerpack/test/loose_files
${LooseFilesClean}           C:/Users/Lucas/Documents/projects/Python/shtickerpack/test/temp_good_files
${LooseFilesDirty}           C:/Users/Lucas/Documents/projects/Python/shtickerpack/test/temp_error_files

*** Test Cases ***
Setup For Good Files
    Setup Loose File Directory    ${LooseFilesClean}

*** Keywords ***
Setup Loose File Directory
    [Arguments]    ${SourceDir}
    [Documentation]    Moves files to a workspace directory.
    Empty Directory     ${LooseFileWorkspace}
    Directory Should Be Empty    ${LooseFileWorkspace}
    Copy Files    ${SourceDir}/*    ${LooseFileWorkspace}
    @{SourceList} =     List Files In Directory     ${SourceDir}
    @{TargetList} =     List Files In Directory     ${LooseFileWorkspace}
    Should Be Equal     ${SourceList}     ${TargetList}

    