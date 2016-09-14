# usefulScripts
Some Scripts I created for automating basic stuff.


## MakefileCreater.py
A Python Script which generates a Makefile for simple C++ Projects. The Makefile is dumped to stdout. 
I mainly use it for updating Dependecies after changing the includes in source files.

## compile.sh oldCompile.cmd
Script to automate Compilation and Running of C++ and Python scripts.
Can be called by editors like Notepad++, Visual Studio Code (Tasks) to perform the task from the editor.


#### Note:
* The path in the scripts are based on my system setup (Windows). They need too be changed.
* `cb_console_runner.exe` is the executable which comes with Code::Blocks. It runs the given program, and waits for keypress after it finishes. Also it shows the time taken by the program.  