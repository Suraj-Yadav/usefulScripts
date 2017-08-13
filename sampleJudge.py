#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reads TestCases from the given File and runs the File on each Test Set
"""

import subprocess
from sys import argv
from sys import platform
from os import path
import argparse


def allowedFiles(choices):
	def CheckExt(choices, fileName):
		if not path.isfile(fileName):
			raise argparse.ArgumentTypeError('File "' + fileName + '" doesn\'t Exist')
		ext = path.splitext(fileName)[1][1:]
		if ext not in choices:
			raise argparse.ArgumentTypeError(
				'Only {} files are supported'.format(choices))
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
