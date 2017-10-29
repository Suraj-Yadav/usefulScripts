#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compiles the given Source Code.
"""

import subprocess
from sys import platform
from os import path
from os import environ
from os import remove
from os import system
from typing import List
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

def isModifiled(inputFileName):

	if not path.exists("." + inputFileName):
		changesNo = system("cp " + inputFileName + " ." + inputFileName)
		return True
	else:
		changesNo = system("diff " + inputFileName + " ." + inputFileName + " >.filechanges")

		if changesNo > 0:
			changesNo = system("cp " + inputFileName + " ." + inputFileName)
			return True
		else:
			return False;

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('file',
                    type=allowedFiles({'cpp', 'c', 'java'}),
                    help='Source File to Compile')

parser.add_argument('buildType', default='COMPILE', nargs='?',
                    choices=['COMPILE', 'DEBUG', 'PROFILE'],
                    help='Type of Build. Only applicable for C/C++ files, ignored otherwise')
args = parser.parse_args()
sourceFile = args.file

(filePathWithoutExt, fileExtension) = path.splitext(sourceFile)

command = []

if fileExtension == '.cpp' or fileExtension == '.c':
	if platform.startswith('win32'):
		targetFile = filePathWithoutExt + '.exe'
	else:
		targetFile = filePathWithoutExt + '.out'

	print(targetFile)

	sourceCode = open(sourceFile, 'r')
	firstLine = sourceCode.readline()
	sourceCode.close()

	includeOptions = []
	linkerOptions = []
	flags = []
	if args.buildType == 'COMPILE':
		flags += ['-O2']
	elif args.buildType == 'DEBUG':
		flags += ['-g']
	elif args.buildType == 'PROFILE':
		flags += ['-O2', '-pg']
	flags += ['-std=c++14', '-Wpedantic', '-Wextra', '-Wall']

	if firstLine == '/*SFML*/':
		includeOptions = ['-IC:\\ExtLibs\\SFML-2.3\\include']
		linkerOptions = ['-LC:\\ExtLibs\\SFML-2.3\\lib',
                   '-lsfml-audio', '-lsfml-network',
                   '-lsfml-graphics', '-lsfml-window',
                   '-lsfml-system']
	if firstLine == "/*OPENGL*/":
		includeOptions = ['-IC:\\ExtLibs\\SFML-2.3\\include',
                    '-IC:\\ExtLibs\\glew-1.12.0\\include',
                    '-IC:\\ExtLibs\\freeglut\\include']
		linkerOptions = ['-LC:\\ExtLibs\\SFML-2.3\\lib',
                   '-LC:\\ExtLibs\\glew-1.12.0\\lib',
                   '-LC:\\ExtLibs\\freeglut\\lib',
                   '-lsfml-audio', '-lsfml-network',
                   '-lsfml-graphics', '-lsfml-window',
                   '-lsfml-system', '-lfreeglut',
                   '-lGLU32', '-lGLEW32', '-lopengl32']

	command = ["g++", '-o', targetFile]
	command += flags
	command += includeOptions
	command += linkerOptions
	command += [sourceFile]

	if path.exists(targetFile) and isModifiled(sourceFile):
		remove(targetFile)

elif fileExtension == '.java':
	command = ["javac", '-Xlint:all', '-cp',
            ';'.join([environ['CLASSPATH'], path.dirname(sourceFile)]),
            sourceFile]

print(*command)
result = subprocess.run(
    command,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    universal_newlines=True)

print(result.stdout)
print(result.stderr[:2000])

if fileExtension == '.java':
	lines = result.stderr.splitlines()  # type: List[str]
	err = []
	i = 0
	# print('sourceFile', sourceFile)
	while i < len(lines):
		# print()
		line = lines[i]
		index = line.find('.java')
		if index != -1:
			# print('line', line)
			# print('line', line[index + 6:])
			# print('FileName', FileName)
			# print('lineNo', lineNo)
			# print('errType', errType)
			# print('message', message)
			FileName = line[index + 5]
			lineNo, errType, message = line[index + 6:].split(':', 2)
			i += 2
			charNo = str(lines[i].index('^') + 1)
			err.append('\n')
			err.append(':'.join([sourceFile, lineNo, charNo, errType, message]))
		elif 'symbol:' in line:
			err.append(': ')
			# print('line', line)
			# print('line', line[line.find(':') + 1:])
			err.append(line[line.find(':') + 1:].strip())
		i += 1
	# print(err)
	print(*err, sep='')
	
