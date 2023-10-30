*** Settings ***
Documentation     The test suite for the shtickerpack engine.
Library    OperatingSystem
Library    Collections
Library    ./lib/clientGUILib.py
Test Tags     repack     GUI
Suite Setup     Repack Suite Setup
Test Setup    Repack Test Setup
Test Teardown    Repack Test Teardown
Test Timeout     10 seconds

*** Variables ***
${ClashResources}            C:/Users/Lucas/AppData/Local/Corporate Clash/resources/contentpacks
${LooseFileWorkspace}        C:/Users/Lucas/Documents/projects/Python/shtickerpack/sandbox/loose_files
${LooseFilesClean}           C:/Users/Lucas/Documents/projects/Python/shtickerpack/sandbox/test_good_files
${LooseFilesDuplicate}       C:/Users/Lucas/Documents/projects/Python/shtickerpack/sandbox/test_dupe_files
${LooseFilesCleanAndDuplicate}     C:/Users/Lucas/Documents/projects/Python/shtickerpack/sandbox/test_good_and_dupe_files
${OutputName}     TEST    
${MinSize}      10000      #10kb

*** Test Cases ***
Repack T0 Without Deletion
    [Tags]    t0
    Setup Loose File Directory    ${LooseFilesClean}
    @{OldFiles} =     List Files In Directory     ${LooseFileWorkspace}
    Setup GUI Repack     deleteFiles=${False}     deleteFolders=${False}
    Start GUI Repack
    Verify Repack
    @{NewFiles} =     List Files In Directory     ${LooseFileWorkspace}
    Should Be Equal     ${OldFiles}     ${NewFiles}

Repack T0 And Delete Files
    [Tags]    t0    delete files
    Setup Loose File Directory    ${LooseFilesClean}
    @{OldFiles} =     List Files In Directory     ${LooseFileWorkspace}
    Setup GUI Repack     deleteFiles=${True}     deleteFolders=${False}
    Start GUI Repack
    Verify Repack
    @{NewFiles} =     List Files In Directory     ${LooseFileWorkspace}
    FOR    ${File}     IN     @{NewFiles}
        Should Not Contain Match     @{NewFiles}     @{OldFiles}
    END

Repack T0 And Delete Folders
    [Tags]    t0    delete folders
    Setup Loose File Directory    ${LooseFilesClean}
    @{OldFiles} =     List Directories In Directory     ${LooseFileWorkspace}
    Setup GUI Repack    deleteFiles=${False}     deleteFolders=${True}
    Start GUI Repack
    Verify Repack
    ${DirCount} =     Count Directories In Directory     ${LooseFileWorkspace}
    Should Be Equal As Numbers    ${DirCount}     0

Repack T0 And Delete Files And Folders
    [Tags]    t0    delete files    delete folders
    Setup Loose File Directory    ${LooseFilesClean}
    Setup GUI Repack     deleteFiles=${True}     deleteFolders=${True}
    Start GUI Repack
    Verify Repack
    ${DirCount} =     Count Directories In Directory     ${LooseFileWorkspace}
    Should Be Equal As Numbers    ${DirCount}     0
    ${FileCount} =     Count Files In Directory     ${LooseFileWorkspace}
    Should Be Equal As Numbers    ${FileCount}     0

Repack T12 Without Deletion
    [Tags]    t12     
    Setup Loose File Directory    ${LooseFilesDuplicate}
    @{OldFiles} =     List Files In Directory     ${LooseFileWorkspace}
    Setup GUI Repack     deleteFiles=${False}     deleteFolders=${False}
    Start GUI Repack
    Verify Repack
    @{NewFiles} =     List Files In Directory     ${LooseFileWorkspace}
    Should Be Equal     ${OldFiles}     ${NewFiles}

Repack T12 And Delete Files
    [Tags]    t12    delete files
    Setup Loose File Directory    ${LooseFilesDuplicate}
    @{OldFiles} =     List Files In Directory     ${LooseFileWorkspace}
    Setup GUI Repack     deleteFiles=${True}     deleteFolders=${False}
    Start GUI Repack
    Verify Repack
    @{NewFiles} =     List Files In Directory     ${LooseFileWorkspace}
    FOR    ${File}     IN     @{NewFiles}
        Should Not Contain Match     @{NewFiles}     @{OldFiles}
    END

Repack T12 And Delete Folders
    [Tags]    t12    delete folders
    Setup Loose File Directory    ${LooseFilesDuplicate}
    Setup GUI Repack     deleteFiles=${False}     deleteFolders=${True}
    Start GUI Repack
    Verify Repack
    ${DirCount} =     Count Directories In Directory     ${LooseFileWorkspace}
    Should Be Equal As Numbers    ${DirCount}     0

Repack T12 And Delete Files And Folders
    [Tags]    t12    delete files    delete folders
    Setup Loose File Directory    ${LooseFilesDuplicate}
    Setup GUI Repack     deleteFiles=${True}     deleteFolders=${True}
    Start GUI Repack
    Verify Repack
    ${DirCount} =     Count Directories In Directory     ${LooseFileWorkspace}
    Should Be Equal As Numbers    ${DirCount}     0
    ${FileCount} =     Count Files In Directory     ${LooseFileWorkspace}
    Should Be Equal As Numbers    ${FileCount}     0

Repack T012 Without Deletion
    [Tags]    t0    t12     
    Setup Loose File Directory    ${LooseFilesCleanAndDuplicate}
    @{OldFiles} =     List Files In Directory     ${LooseFileWorkspace}
    Setup GUI Repack     deleteFiles=${False}     deleteFolders=${False}
    Start GUI Repack
    Verify Repack
    @{NewFiles} =     List Files In Directory     ${LooseFileWorkspace}
    Should Be Equal     ${OldFiles}     ${NewFiles}

Repack T012 And Delete Files
    [Tags]    t0    t12    delete files
    Setup Loose File Directory    ${LooseFilesCleanAndDuplicate}
    @{OldFiles} =     List Files In Directory     ${LooseFileWorkspace}
    Setup GUI Repack     deleteFiles=${True}     deleteFolders=${False}
    Start GUI Repack
    Verify Repack
    @{NewFiles} =     List Files In Directory     ${LooseFileWorkspace}
    FOR    ${File}     IN     @{NewFiles}
        Should Not Contain Match     @{NewFiles}     @{OldFiles}
    END

Repack T012 And Delete Folders
    [Tags]    t0    t12    delete folders
    Setup Loose File Directory    ${LooseFilesCleanAndDuplicate}
    Setup GUI Repack     deleteFiles=${False}     deleteFolders=${True}
    Start GUI Repack
    Verify Repack
    ${DirCount} =     Count Directories In Directory     ${LooseFileWorkspace}
    Should Be Equal As Numbers    ${DirCount}     0

Repack T012 And Delete Files And Folders
    [Tags]    t0    t12    delete files    delete folders
    Setup Loose File Directory    ${LooseFilesCleanAndDuplicate}
    Setup GUI Repack     deleteFiles=${True}     deleteFolders=${True}
    Start GUI Repack
    Verify Repack
    ${DirCount} =     Count Directories In Directory     ${LooseFileWorkspace}
    Should Be Equal As Numbers    ${DirCount}     0
    ${FileCount} =     Count Files In Directory     ${LooseFileWorkspace}
    Should Be Equal As Numbers    ${FileCount}     0



*** Keywords ***
Repack Suite Setup
    Set Log Level     DEBUG

Repack Test Setup
    Remove File     ${ClashResources}/${OutputName}.mf
    Empty Directory     ${LooseFileWorkspace}

Repack Test Teardown
    Remove File     ${ClashResources}/${OutputName}.mf
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

Setup GUI Repack
    [Arguments]     ${deleteFiles}     ${deleteFolders}
    Select Tab     tab=1
    Set Repack Input     fp=${LooseFileWorkspace}
    Set Repack Output Name     name=${OutputName}
    Set Repack Deletion Mode     deleteFiles=${DeleteFiles}     deleteFolders=${DeleteFolders}

Verify Repack
    [Arguments]    ${timeout}=10 seconds        ${minSize}=${MinSize}
    [Documentation]     Verifies OutputName exists in OutputDir. OutputName must include the file extension.
    Verify No Modals
    Wait Until Created     ${ClashResources}/${OutputName}.mf     timeout=${timeout}
    ${Size} =     Get File Size      ${ClashResources}/${OutputName}.mf
    Should Be True     ${Size} > ${minSize}
    