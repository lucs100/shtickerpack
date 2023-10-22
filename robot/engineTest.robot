*** Settings ***
Documentation     The test suite for the shtickerpack engine.
Library    OperatingSystem
Library    Collections
Library    ./lib/engineLib.py
Test Setup    Custom Test Setup
Test Teardown    Custom Test Teardown

*** Variables ***
${ClashResources}            C:/Users/Lucas/AppData/Local/Corporate Clash/resources/contentpacks
${LooseFileWorkspace}        C:/Users/Lucas/Documents/projects/Python/shtickerpack/test/loose_files
${LooseFilesClean}           C:/Users/Lucas/Documents/projects/Python/shtickerpack/test/temp_good_files
${LooseFilesDirty}           C:/Users/Lucas/Documents/projects/Python/shtickerpack/test/temp_error_files
${True}     True
${False}    False

*** Test Cases ***
Repack Clean Files Without Deletion
    [Tags]    repack    clean
    Setup Loose File Directory    ${LooseFilesClean}
    @{OldFiles} =     List Files In Directory     ${LooseFileWorkspace}
    Repack Loose Files     deleteFiles=${False}     deleteFolders=${False}
    Verify Packed Output Exists
    @{NewFiles} =     List Files In Directory     ${LooseFileWorkspace}
    Should Be Equal     ${OldFiles}     ${NewFiles}

Repack Clean Files And Delete Files
    [Tags]    repack    clean    delete files
    Setup Loose File Directory    ${LooseFilesClean}
    @{OldFiles} =     List Files In Directory     ${LooseFileWorkspace}
    Repack Loose Files     deleteFiles=${True}     deleteFolders=${False}
    Verify Packed Output Exists
    @{NewFiles} =     List Files In Directory     ${LooseFileWorkspace}
    FOR    ${File}     IN     @{NewFiles}
        Should Not Contain Match     @{NewFiles}     @{OldFiles}
    END

Repack Clean Files And Delete Folders
    [Tags]    repack    clean    delete folders
    Setup Loose File Directory    ${LooseFilesClean}
    @{OldFiles} =     List Directories In Directory     ${LooseFileWorkspace}
    Repack Loose Files     deleteFiles=${False}     deleteFolders=${True}
    Verify Packed Output Exists
    ${DirCount} =     Count Directories In Directory     ${LooseFileWorkspace}
    Should Be Equal As Numbers    ${DirCount}     0

Repack Clean Files And Delete Files And Folders
    [Tags]    repack    clean    delete files    delete folders
    Setup Loose File Directory    ${LooseFilesClean}
    @{OldFiles} =     List Directories In Directory     ${LooseFileWorkspace}
    Repack Loose Files     deleteFiles=${True}     deleteFolders=${True}
    Verify Packed Output Exists
    ${DirCount} =     Count Directories In Directory     ${LooseFileWorkspace}
    Should Be Equal As Numbers    ${DirCount}     0
    ${FileCount} =     Count Files In Directory     ${LooseFileWorkspace}
    Should Be Equal As Numbers    ${FileCount}     0


*** Keywords ***
Custom Test Setup
    Remove File     ${ClashResources}/_TEST.mf
    Empty Directory     ${LooseFileWorkspace}

Custom Test Teardown
    Remove File     ${ClashResources}/_TEST.mf
    Empty Directory     ${LooseFileWorkspace}

Setup Loose File Directory
    [Arguments]    ${SourceDir}
    [Documentation]    Moves files to a workspace directory to prepare a packing test.
    Empty Directory     ${LooseFileWorkspace}
    Directory Should Be Empty    ${LooseFileWorkspace}
    Copy Files    ${SourceDir}/*    ${LooseFileWorkspace}
    @{SourceList} =     List Files In Directory     ${SourceDir}
    @{TargetList} =     List Files In Directory     ${LooseFileWorkspace}
    Should Be Equal     ${SourceList}     ${TargetList}

Verify Packed Output Exists
    [Arguments]    ${OutputDir}=${ClashResources}     ${OutputName}=_TEST
    [Documentation]     Verifies OutputName exists in OutputDir. OutputName must include the file extension.
    File Should Exist     ${OutputDir}/${OutputName}.mf
    