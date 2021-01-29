@ECHO OFF
SETLOCAL
SET _NT_SYMBOL_PATH=

IF "%~1" == "--all" (
  REM If you can add the x86 and x64 binaries of python to the path, or add links to the local folder, tests will be run
  REM in both
  WHERE PYTHON_X86 >nul 2>&1
  IF NOT ERRORLEVEL 0 (
    ECHO - PYTHON_X86 was not found; not testing both x86 and x64 ISAs.
  ) ELSE (
    WHERE PYTHON_X64 >nul 2>&1
    IF NOT ERRORLEVEL 0 (
      ECHO - PYTHON_X64 was not found; not testing both x86 and x64 ISAs.
    ) ELSE (
      GOTO :TEST_BOTH_ISAS
    )
  )
)

WHERE PYTHON 2>&1 >nul
IF ERRORLEVEL 1 (
  ECHO - PYTHON was not found!
  ENDLOCAL
  EXIT /B 1
)

ECHO * Running tests in unknown build of Python...
CALL PYTHON "%~dpn0\%~n0.py" %*
IF ERRORLEVEL 1 GOTO :ERROR
GOTO :ADDITIONAL_TESTS

:TEST_BOTH_ISAS
  ECHO * Running tests in x86 build of Python...
  CALL PYTHON_X86 "%~dpn0\%~n0.py" %*
  IF ERRORLEVEL 1 GOTO :ERROR
  ECHO * Running tests in x64 build of Python...
  CALL PYTHON_X64 "%~dpn0\%~n0.py" %*
  IF ERRORLEVEL 1 GOTO :ERROR
  ENDLOCAL
  EXIT /B 0

:ADDITIONAL_TESTS
SET TEST_FOLDER_PATH=%TEMP%\FileSystemBrowser Test folder %RANDOM%

MKDIR "%TEST_FOLDER_PATH%"

ECHO   * Test version check...
CALL "%~dp0FileSystemBrowser.cmd" --version
IF ERRORLEVEL 1 GOTO :ERROR

ECHO   * Test help...
CALL "%~dp0FileSystemBrowser.cmd" --help
IF ERRORLEVEL 1 GOTO :ERROR

ECHO   * Test offline...
CALL "%~dp0FileSystemBrowser.cmd" "%~dpn0" --offline="%TEST_FOLDER_PATH%"
IF ERRORLEVEL 1 GOTO :ERROR
ECHO   * Test offline with sharepoint hacks... 
CALL "%~dp0FileSystemBrowser.cmd" "%~dpn0" --offline="%TEST_FOLDER_PATH%" --apply-sharepoint-hacks
IF ERRORLEVEL 1 GOTO :ERROR

RD "%TEST_FOLDER_PATH%" /S /Q

ECHO + Done.
ENDLOCAL
EXIT /B 0

:ERROR
  ECHO     - Failed with error level %ERRORLEVEL%
  IF EXIST "%TEST_FOLDER_PATH%" RD "%TEST_FOLDER_PATH%" /S /Q
  ENDLOCAL
  EXIT /B 1
