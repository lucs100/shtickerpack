*** Settings ***
Documentation     The test suite for the shtickerpack engine.
Library    OperatingSystem
Library    Collections
Library    ./lib/engineLib.py
Test Setup    Custom Test Setup
Test Teardown    Custom Test Teardown

*** Variables ***
${ClashResources}            C:/Users/Lucas/AppData/Local/Corporate Clash/resources/contentpacks
${LooseFileWorkspace}        C:/Users/Lucas/Documents/projects/Python/shtickerpack/sandbox/loose_files
${LooseFilesClean}           C:/Users/Lucas/Documents/projects/Python/shtickerpack/sandbox/temp_good_files
${LooseFilesDuplicate}       C:/Users/Lucas/Documents/projects/Python/shtickerpack/sandbox/temp_dupe_files
${LooseFilesCleanAndDuplicate}     C:/Users/Lucas/Documents/projects/Python/shtickerpack/sandbox/temp_good_and_dupe_files
${True}     True
${False}    False

*** Test Cases ***
Repack T0 Without Deletion
    [Tags]    repack    t0
    Setup Loose File Directory    ${LooseFilesClean}
    @{OldFiles} =     List Files In Directory     ${LooseFileWorkspace}
    Repack Loose Files     deleteFiles=${False}     deleteFolders=${False}
    Verify Packed Output Exists
    @{NewFiles} =     List Files In Directory     ${LooseFileWorkspace}
    Should Be Equal     ${OldFiles}     ${NewFiles}

Repack T0 And Delete Files
    [Tags]    repack    t0    delete files
    Setup Loose File Directory    ${LooseFilesClean}
    @{OldFiles} =     List Files In Directory     ${LooseFileWorkspace}
    Repack Loose Files     deleteFiles=${True}     deleteFolders=${False}
    Verify Packed Output Exists
    @{NewFiles} =     List Files In Directory     ${LooseFileWorkspace}
    FOR    ${File}     IN     @{NewFiles}
        Should Not Contain Match     @{NewFiles}     @{OldFiles}
    END

Repack T0 And Delete Folders
    [Tags]    repack    t0    delete folders
    Setup Loose File Directory    ${LooseFilesClean}
    @{OldFiles} =     List Directories In Directory     ${LooseFileWorkspace}
    Repack Loose Files     deleteFiles=${False}     deleteFolders=${True}
    Verify Packed Output Exists
    ${DirCount} =     Count Directories In Directory     ${LooseFileWorkspace}
    Should Be Equal As Numbers    ${DirCount}     0

Repack T0 And Delete Files And Folders
    [Tags]    repack    t0    delete files    delete folders
    Setup Loose File Directory    ${LooseFilesClean}
    Repack Loose Files     deleteFiles=${True}     deleteFolders=${True}
    Verify Packed Output Exists
    ${DirCount} =     Count Directories In Directory     ${LooseFileWorkspace}
    Should Be Equal As Numbers    ${DirCount}     0
    ${FileCount} =     Count Files In Directory     ${LooseFileWorkspace}
    Should Be Equal As Numbers    ${FileCount}     0

Repack T12 Without Deletion
    [Tags]    repack     t12     
    Setup Loose File Directory    ${LooseFilesDuplicate}
    @{OldFiles} =     List Files In Directory     ${LooseFileWorkspace}
    Repack Loose Files     deleteFiles=${False}     deleteFolders=${False}
    Verify Packed Output Exists
    @{NewFiles} =     List Files In Directory     ${LooseFileWorkspace}
    Should Be Equal     ${OldFiles}     ${NewFiles}

Repack T12 And Delete Files
    [Tags]    repack    t12    delete files
    Setup Loose File Directory    ${LooseFilesDuplicate}
    @{OldFiles} =     List Files In Directory     ${LooseFileWorkspace}
    Repack Loose Files     deleteFiles=${True}     deleteFolders=${False}
    Verify Packed Output Exists
    @{NewFiles} =     List Files In Directory     ${LooseFileWorkspace}
    FOR    ${File}     IN     @{NewFiles}
        Should Not Contain Match     @{NewFiles}     @{OldFiles}
    END

Repack T12 And Delete Folders
    [Tags]    repack    t12    delete folders
    Setup Loose File Directory    ${LooseFilesDuplicate}
    Repack Loose Files     deleteFiles=${False}     deleteFolders=${True}
    Verify Packed Output Exists
    ${DirCount} =     Count Directories In Directory     ${LooseFileWorkspace}
    Should Be Equal As Numbers    ${DirCount}     0

Repack T12 And Delete Files And Folders
    [Tags]    repack    t12    delete files    delete folders
    Setup Loose File Directory    ${LooseFilesDuplicate}
    Repack Loose Files     deleteFiles=${True}     deleteFolders=${True}
    Verify Packed Output Exists
    ${DirCount} =     Count Directories In Directory     ${LooseFileWorkspace}
    Should Be Equal As Numbers    ${DirCount}     0
    ${FileCount} =     Count Files In Directory     ${LooseFileWorkspace}
    Should Be Equal As Numbers    ${FileCount}     0


Repack T012 Without Deletion
    [Tags]    repack     t0    t12     
    Setup Loose File Directory    ${LooseFilesCleanAndDuplicate}
    @{OldFiles} =     List Files In Directory     ${LooseFileWorkspace}
    Repack Loose Files     deleteFiles=${False}     deleteFolders=${False}
    Verify Packed Output Exists
    @{NewFiles} =     List Files In Directory     ${LooseFileWorkspace}
    Should Be Equal     ${OldFiles}     ${NewFiles}

Repack T012 And Delete Files
    [Tags]    repack    t0    t12    delete files
    Setup Loose File Directory    ${LooseFilesCleanAndDuplicate}
    @{OldFiles} =     List Files In Directory     ${LooseFileWorkspace}
    Repack Loose Files     deleteFiles=${True}     deleteFolders=${False}
    Verify Packed Output Exists
    @{NewFiles} =     List Files In Directory     ${LooseFileWorkspace}
    FOR    ${File}     IN     @{NewFiles}
        Should Not Contain Match     @{NewFiles}     @{OldFiles}
    END

Repack T012 And Delete Folders
    [Tags]    repack    t0    t12    delete folders
    Setup Loose File Directory    ${LooseFilesCleanAndDuplicate}
    Repack Loose Files     deleteFiles=${False}     deleteFolders=${True}
    Verify Packed Output Exists
    ${DirCount} =     Count Directories In Directory     ${LooseFileWorkspace}
    Should Be Equal As Numbers    ${DirCount}     0

Repack T012 And Delete Files And Folders
    [Tags]    repack    t0    t12    delete files    delete folders
    Setup Loose File Directory    ${LooseFilesCleanAndDuplicate}
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
    