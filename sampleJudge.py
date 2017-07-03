#!/usr/bin/env python3
""" Runs the Program on the given TestCases """

import subprocess
from sys import argv
from sys import platform
from sys import stdout
from sys import stdin
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
	command = ["python3", argv[1]]
elif file_extension == ".c" or file_extension == ".cpp":
	if platform.startswith('win32'):
		command = [filename + '.exe']
	else:
		command = [filename + '.out']

while i < len(sampleTestCases) and "***/" not in sampleTestCases[i]:
	inputString = ""
	while (i < len(sampleTestCases) and sampleTestCases[i] != "\n" and
                "***/" not in sampleTestCases[i]):
		inputString += sampleTestCases[i]
		i += 1
	if i < len(sampleTestCases) and "***/" in sampleTestCases[i]:
		break
	else:
		i += 1
	if inputString == "":
		continue
	# print(inputString)
	program = subprocess.Popen(command, stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, universal_newlines=True)
	o = program.communicate(inputString)
	print("############")
	# print(inputString)
	print(o[0])
	print("returned", program.returncode)
	t += 1
