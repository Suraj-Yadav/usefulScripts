# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 22:58:56 2016
A simple Python Scripts which generates a Makefile for simple C++ Projects.
@author: Suraj
"""

import os
import subprocess

CPP_FLAGS = '-g -Wunreachable-code -std=c++11 -Wextra -Wall '
INCLUDE = '-IC:/ExtLibs/SFML-2.3/include '
LINK = '-LC:/ExtLibs/SFML-2.3/lib '
LINK_SYM = '-lopengl32 -lsfml-graphics -lsfml-window -lsfml-system -lsfml-audio -lsfml-network '


def getFileDepedndecies(cppFile):
	os.chdir(mypath)
	print('# Rules for ' + cppFile)
	proc = subprocess.Popen('g++ -MM ' + cppFile, stdout=subprocess.PIPE,
							stderr=subprocess.PIPE, universal_newlines=True)

	try:
		output, errors = proc.communicate(timeout=15)
	except subprocess.	TimeoutExpired:
		proc.kill()
		output, errors = proc.communicate()

	if proc.returncode == 0:
		file, dependecies = output.split(':')
		dependecies = dependecies.split()
		while '\\' in dependecies:
			dependecies.remove('\\')
		return (file, dependecies)

	return ''


def compileCommand(file):
	fileName = file[:-2]
	print('\tg++ ' + CPP_FLAGS + INCLUDE + ' -c ' +
		  fileName + '.cpp -o obj/' + fileName + '.o\n')


def buildCommand(file, dependecies):
	str = '\tg++ ' + LINK + ' -o ' + file
	for i in dependecies:
		str += ' ' + i
	str += ' ' + LINK_SYM
	print(str + '\n')


def writeRule(stream, file, dependecies):
	str = file + ' :'
	for i in dependecies:
		str += ' ' + i
	print(str)


def generateExecDependecies(mypath):
	executableFile = 'bin/' + mypath.rsplit('\\', 1)[1] + '.exe'
	executableDependecies = []
	print('all: ' + executableFile)
	files = os.listdir(mypath)
	for file in files:
		if not os.path.isdir(mypath + '/' + file) and file.endswith('.cpp'):
			objectFile, dependecies = getFileDepedndecies(file)
			executableDependecies.append('obj/' + objectFile)
			writeRule(None, 'obj/' + objectFile, dependecies)
			print('\tcmd /c if not exist obj md obj')
			compileCommand(objectFile)

	writeRule(None, executableFile, executableDependecies)
	print('\tcmd /c if not exist bin md bin')
	buildCommand(executableFile, executableDependecies)

	print('RUN : ', executableFile)
	print('\t', 'cmd /c start "" "C:/ExtLibs/cb_console_runner.exe"',executableFile, '\n')


def clean():
	print('CLEAN:')
	print('\tcmd /c if exist bin rd /S /Q bin')
	print('\tcmd /c if exist obj rd /S /Q obj')
	print('\n')

def cppCheck():
	print('CPPCHECK:')
	print('\t"G:\Program Files\Cppcheck\cppcheck.exe" --enable=all --template=gcc -q .')
	print('\n')

mypath = os.getcwd()
generateExecDependecies(mypath)
clean()
cppCheck()
