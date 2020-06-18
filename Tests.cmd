@ECHO OFF
SETLOCAL
SET TEST_FOLDER_PATH=%TEMP%\FileSystemBrowser Test folder %RANDOM%
SET TEST_ZIP_FILE_PATH=%TEMP%\zyp Test file %RANDOM%.zip

MKDIR "%TEST_FOLDER_PATH%"

ECHO   * Test version check...
CALL "%~dp0FileSystemBrowser.cmd" --version
IF ERRORLEVEL 1 GOTO :ERROR

ECHO   * Test help...
CALL "%~dp0FileSystemBrowser.cmd" --help
IF ERRORLEVEL 1 GOTO :ERROR

ECHO   * Test offline...
CALL "%~dp0FileSystemBrowser.cmd" --offline="%TEST_FOLDER_PATH%"
IF ERRORLEVEL 1 GOTO :ERROR
ECHO   * Test offline with sharepoint hacks... 
CALL "%~dp0FileSystemBrowser.cmd" --offline="%TEST_FOLDER_PATH%" --apply-sharepoint-hacks
IF ERRORLEVEL 1 GOTO :ERROR

RD "%TEST_FOLDER_PATH%" /S /Q

ECHO + Done.
EXIT /B 0

:ERROR
  ECHO     - Failed with error level %ERRORLEVEL%
  IF EXIST "%TEST_FOLDER_PATH%" RD "%TEST_FOLDER_PATH%" /S /Q
  ENDLOCAL
  EXIT /B 1
