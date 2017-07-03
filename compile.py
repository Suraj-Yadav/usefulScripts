#!/usr/bin/env python3
""" Compiles the Source Code """

import subprocess
from sys import argv
from sys import platform
from os import path
from os import environ
from os import remove

if len(argv) != 2:
	print("ERROR")
	print("Usage: compile.py <FileName>")
	exit()

sourceFile = argv[1]
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
	flags = ['-g', '-std=c++14', '-Wpedantic', '-Wextra', '-Wall']

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

	if path.exists(targetFile):
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
