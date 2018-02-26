#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reads TestCases from the given File and runs the File on each Test Set
"""

import subprocess
import argparse
from sys import platform, stdout
from os import path
from colorama import init, Fore
from tabulate import tabulate

if stdout.isatty():
	init()


def allowedFiles(choices):
	def CheckExt(choices, fileName):
		if not path.isfile(fileName):
			raise argparse.ArgumentTypeError(f'File "{fileName}" doesn\'t Exist')
		ext = path.splitext(fileName)[1][1:]
		if ext not in choices:
			raise argparse.ArgumentTypeError(f'Only {choices} type files are supported')
		return fileName
	return lambda fileName: CheckExt(choices, fileName)


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('file',
                    type=allowedFiles({'py', 'cpp', 'c', 'java'}),
                    help='Source File to Test')
sourceFile = parser.parse_args().file

sampleTestCases = open(sourceFile).readlines()

i = 0
while i < len(sampleTestCases) and sampleTestCases[i] != "/***\n":
	i += 1

if i == len(sampleTestCases):
	print("No TestCase found in file:", sourceFile)
	exit()

i += 1

filename, file_extension = path.splitext(sourceFile)

if file_extension == ".java":
	command = ["java", filename]
elif file_extension == ".py":
	command = ["python3", sourceFile]
elif file_extension == ".c" or file_extension == ".cpp":
	if platform.startswith('win32'):
		command = [filename + '.exe']
	else:
		command = [filename + '.out']

headers = ["input", "expected", "actual"]
table = []

totalTestCases = 0
passedTestCases = 0
failedTestCases = 0
ignoredTestCases = 0


def colorThis(string: str, color: str):
	return (color +
         (Fore.RESET + '\n' + color).join(string.split('\n')) +
            Fore.RESET)


while i < len(sampleTestCases) and "***/" not in sampleTestCases[i]:
	inputString = ""
	outputString = ""
	while (i < len(sampleTestCases) and
                sampleTestCases[i] != "\n" and
                "***/" not in sampleTestCases[i] and
                "---" not in sampleTestCases[i]):
		inputString += sampleTestCases[i]
		i += 1

	if "---" in sampleTestCases[i]:
		i += 1

	while (i < len(sampleTestCases) and
                sampleTestCases[i] != "\n" and
                "***/" not in sampleTestCases[i]):
		outputString += sampleTestCases[i]
		i += 1

	if i < len(sampleTestCases) and "***/" in sampleTestCases[i]:
		break
	else:
		i += 1
	if inputString == "":
		continue
	totalTestCases += 1
	program = subprocess.Popen(command,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            universal_newlines=True)
	o = program.communicate(inputString)
	returnCode = program.returncode

	outputString = '\n'.join(list(map(str.strip, outputString.split('\n'))))
	actualString = '\n'.join(list(map(str.strip, o[0].split('\n'))))

	if returnCode == 0 and outputString == "":
		ignoredTestCases += 1
		textColor = Fore.RESET
	elif returnCode == 0 and actualString == outputString:
		passedTestCases += 1
		textColor = Fore.GREEN
	else:
		failedTestCases += 1
		textColor = Fore.RED

	table.append([colorThis(inputString, textColor),
               colorThis(outputString, textColor),
               colorThis(o[0] +
                         ('' if returnCode == 0 else 'returned ' +
                          str(returnCode)), textColor)])

print(tabulate(table, headers, tablefmt="grid"))

if ignoredTestCases + passedTestCases == totalTestCases:
	print(Fore.GREEN, "PASSED", passedTestCases, '/', totalTestCases)
else:
	print(Fore.RED, "FAILED", failedTestCases, '/', totalTestCases)
