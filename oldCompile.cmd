@ECHO OFF
IF "%~1" == "" GOTO NO_FILE
IF "%2" == "" GOTO NO_FILE

for /f "tokens=1,2 delims=." %%a in ("%~1") do set FileName=%%a&set Ext=%%b

GOTO %2

:COMPILE
@Echo Compiling %1

GOTO COMPILE_%Ext%

:COMPILE_cpp
for /f "tokens=1,2 delims=" %%i in ('C:\\Progra~1\\Git\\usr\\bin\\head.exe -n1 %1') do set TYPE=%%i&set OUTPUT=%%j

REM @Echo "%TYPE%"

IF "%TYPE%" == "/*SFML*/" GOTO SFML_OPTION
IF "%TYPE%" == "/*OPENGL*/" GOTO OPENGL_OPTION

set INCLUDEOPTIONS=
set LINKEROPTIONS=
GOTO SKIP_CPP_OPTIONS

:SFML_OPTION
set INCLUDEOPTIONS=-IC:\ExtLibs\SFML-2.3\include
set LINKEROPTIONS=-LC:\ExtLibs\SFML-2.3\lib -lsfml-audio -lsfml-network -lsfml-graphics -lsfml-window -lsfml-system
GOTO SKIP_CPP_OPTIONS

:OPENGL_OPTION
set INCLUDEOPTIONS=-IC:\ExtLibs\SFML-2.3\include -IC:\ExtLibs\glew-1.12.0\include
set LINKEROPTIONS=-LC:\ExtLibs\SFML-2.3\lib -LC:\ExtLibs\glew-1.12.0\lib -lsfml-audio -lsfml-network -lsfml-graphics -lsfml-window -lsfml-system -lGLU32 -lGLEW32 -lopengl32
GOTO SKIP_CPP_OPTIONS

:SKIP_CPP_OPTIONS
IF EXIST "G:\work\c++_progs\a.exe" DEL "G:\work\c++_progs\a.exe"
IF EXIST "G:\work\c++_progs\a.o" DEL "G:\work\c++_progs\a.o"

g++.exe -g -Wunreachable-code -std=c++11 -pedantic -Wextra -Wall %INCLUDEOPTIONS% -c "%FileName%.%Ext%" -o "G:\work\c++_progs\a.o"

IF %ERRORLEVEL% == 1 GOTO COMPILE_EXIT

g++.exe -o "G:\work\c++_progs\a.exe" "G:\work\c++_progs\a.o" %LINKEROPTIONS%

GOTO COMPILE_EXIT

:COMPILE_java
%JAVA_HOME%\bin\javac -cp %CP% "%FileName%.%Ext%" -Xlint

GOTO COMPILE_EXIT

:COMPILE_EXIT
IF %ERRORLEVEL% == 1 @ECHO Compilation Failed
IF %ERRORLEVEL% == 0 @ECHO Compilation Complete
GOTO EXIT

:RUN

GOTO RUN_%Ext%

:RUN_cpp
IF NOT EXIST "G:\work\c++_progs\a.exe" ECHO ERROR:10:1: error WHO WILL COMPILE?
IF NOT EXIST "G:\work\c++_progs\a.exe" GOTO EXIT
start "%FileName%" "C:\ExtLibs\cb_console_runner.exe" "G:\work\c++_progs\a.exe"
GOTO RUN_EXIT

:RUN_java
start "" "C:\ExtLibs\cb_console_runner.exe" %JAVA_HOME%\bin\javac -cp %CP% "%FileName%"
GOTO RUN_EXIT

:RUN_py
start "%FileName%" "C:\ExtLibs\cb_console_runner.exe" python "%FileName%.%Ext%"
GOTO RUN_EXIT

:RUN_EXIT
@Echo Run Complete
GOTO EXIT

:CPPCHECK
"G:\Program Files\Cppcheck\cppcheck.exe" --enable=all --template=gcc "%FileName%.%Ext%"

GOTO EXIT

:NO_FILE
@Echo Usage: Compile[.cmd] FileName (COMPILE^|RUN)


:EXIT