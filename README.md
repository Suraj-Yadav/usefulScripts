# usefulScripts
Some Scripts I created for automating basic stuff.

## compile.py compile.sh oldCompile.cmd
Script to automate Compilation and Running of C++, Java and Python scripts.
Switched to Python3, as it was easier to work with than Shell Scripts.
Python Script process the output of `javac` to add Column No in warnings and error.
Can be called by editors like Notepad++, Visual Studio Code (using Tasks) to perform the task from the editor.


## sampleJudge.py
Script to automate running of TestCases for Competitive Coding. The test cases are read from the Source Code, and the script based on the Language used, chooses the correct commands for running the program.


#### Note:
* The path in the scripts are based on my system setup (Windows). They need to be changed.
* `cb_console_runner.exe` is the executable which comes with Code::Blocks. It runs the given program, and waits for keypress after it finishes. Also it shows the time taken by the program.  
