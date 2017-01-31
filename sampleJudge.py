""" Runs the Program on the given TestCases """

import subprocess
from sys import argv
from sys import platform
from os import path

if len(argv) != 2:
	print("ERROR")
	print("Usage: python3 sampleJudge.py <FileName>")
	exit()

sampleTestCases = open(argv[1]).readlines()

# print(sampleTestCases)

i = 0
while i < len(sampleTestCases) and sampleTestCases[i] != "/***\n":
	i += 1

if i == len(sampleTestCases):
	print("No TestCase found in file:", argv[1])
	exit()

i += 1
t = 1

filename, file_extension = path.splitext(argv[1])

if file_extension == ".java":
	command = ["java", filename]
elif file_extension == ".py":
	command = ["python", argv[1]]		#Note Change this to python3 if you code in that
elif file_extension == ".c" or file_extension == ".cpp":
	if platform.startswith('win32'):
		command = ["a.exe"]
	else:
		command = ["./a.out"]

while i < len(sampleTestCases) and sampleTestCases[i] != "***/\n":
	inputString = ""
	while i < len(sampleTestCases) and sampleTestCases[i] != "\n" and sampleTestCases[i] != "***/\n":
		inputString += sampleTestCases[i]
		i += 1
	if i < len(sampleTestCases) and sampleTestCases[i] == "***/\n":
		i = len(sampleTestCases)
	else:
		i += 1
	if inputString == "":
		continue
	program = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
	o = program.communicate(inputString)
	print("############")
	print(o[0])
	t += 1
