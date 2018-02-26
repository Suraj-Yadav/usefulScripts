# usefulScripts
Some Scripts I created for automating basic stuff.

## compile.py
Script to automate Compilation and Running of C++, Java and Python scripts.
Switched to Python3, as it was easier to work with than Shell Scripts.
Python Script process the output of `javac` to add Column Number in warnings and error.
Can be called by editors like [Notepad++](https://notepad-plus-plus.org/news/notepad-7.3-released.html), [Visual Studio Code](https://code.visualstudio.com/) (using Tasks) to perform the task from the editor.


## sampleJudge.py
Script to automate running of TestCases for Competitive Coding. The test cases are read from the Source Code, and the script based on the Language used, chooses the correct commands for running the program.


## testCaseDownloader.py
Script to automate downloading of TestCases for Competitive Coding. Currently supports only [Codeforces](http://codeforces.com). Can be configured to work with any configuration by editing the functions `getURLFromFile` and `whatToDoWithTestCase`.