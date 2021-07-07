@ECHO OFF
SETLOCAL
SET REDIRECT_STDOUT_FILE_PATH=%TEMP%\BugId Test stdout %RANDOM%.txt
SET TEST_FOLDER_PATH=%TEMP%\FileSystemBrowser Test folder %RANDOM%

ECHO   * Test usage help...
CALL "%~dp0\..\FileSystemBrowser.cmd" --help >"%REDIRECT_STDOUT_FILE_PATH%"
IF ERRORLEVEL 1 GOTO :ERROR
ECHO   * Test version info...
CALL "%~dp0\..\FileSystemBrowser.cmd" --version >"%REDIRECT_STDOUT_FILE_PATH%"
IF ERRORLEVEL 1 GOTO :ERROR
ECHO   * Test version check...
CALL "%~dp0\..\FileSystemBrowser.cmd" --version-check >"%REDIRECT_STDOUT_FILE_PATH%"
IF ERRORLEVEL 1 GOTO :ERROR
ECHO   * Test license info...
CALL "%~dp0\..\FileSystemBrowser.cmd" --license >"%REDIRECT_STDOUT_FILE_PATH%"
IF ERRORLEVEL 1 GOTO :ERROR
ECHO   * Test license update...
CALL "%~dp0\..\FileSystemBrowser.cmd" --license-update >"%REDIRECT_STDOUT_FILE_PATH%"
IF ERRORLEVEL 1 GOTO :ERROR
DEL "%REDIRECT_STDOUT_FILE_PATH%" /Q

MKDIR "%TEST_FOLDER_PATH%"

ECHO   * Test offline...
CALL "%~dp0\..\FileSystemBrowser.cmd" "%~dp0." --offline="%TEST_FOLDER_PATH%"
IF ERRORLEVEL 1 GOTO :ERROR

RD "%TEST_FOLDER_PATH%" /S /Q

ECHO + Test.cmd completed.
ENDLOCAL
EXIT /B 0

:ERROR
  ECHO     - Failed with error level %ERRORLEVEL%
  CALL :CLEANUP
  ENDLOCAL
  EXIT /B 3

:CLEANUP
  IF EXIST "%TEST_FOLDER_PATH%" (
    RD "%TEST_FOLDER_PATH%" /S /Q
  )
  IF EXIST "%REDIRECT_STDOUT_FILE_PATH%" (
    TYPE "%REDIRECT_STDOUT_FILE_PATH%"
    DEL "%REDIRECT_STDOUT_FILE_PATH%" /Q
  )
