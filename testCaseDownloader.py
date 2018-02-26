#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Downloads TestCases from websites.
"""

import argparse
from typing import List, Tuple

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('file', help='Source File to get TestCases for')
file = parser.parse_args().file


def getTestCasesFromWebPage(url: str):
	import requests
	from bs4 import BeautifulSoup

	r = requests.get(url)
	if 'codeforces' in url:
		soup = BeautifulSoup(r.text, 'html.parser')
		inputs = soup.find_all('div', {'class': 'input'})
		outputs = soup.find_all('div', {'class': 'output'})
		ret = []
		for i, o in zip(inputs, outputs):
			ret.append(('\n'.join(i.find('pre').find_all(text=True)),
                            '\n'.join(o.find('pre').find_all(text=True))))
		return ret
	elif 'csacademy' in url:
		# CSAcademy has dynamically created WebPages. Too much effort
		return []
	elif 'codechef' in url:
		# Codechef has dynamically created WebPages. Too much effort
		return []
	else:
		return []


# ########################################################################


def getURLFromFile(sourceFile: str):
	'''
	Generates the url for problem statement from the fileName, content etc.
	'''
	from os import path
	from string import ascii_uppercase

	baseName = path.splitext(path.basename(sourceFile))[0]  # type:str
	parts = baseName.split('_')
	if parts[0].isdecimal() and parts[1] in ascii_uppercase:
		# This is my format for Codeforces file
		return f'http://codeforces.com/contest/{parts[0]}/problem/{parts[1]}'
	else:
		return f''


def whatToDoWithTestCase(testCases: List[Tuple[str]]):
	'''
	What To Do With TestCases
	'''
	import pyperclip

	if len(testCases) > 0:
		stringToClipBoard = '\n'
		for i, o in testCases:
			stringToClipBoard += i
			stringToClipBoard += '\n---\n'
			stringToClipBoard += o
			stringToClipBoard += '\n\n'
		pyperclip.copy(stringToClipBoard)


def main(sourceFile: str):
	url = getURLFromFile(sourceFile)
	testCases = getTestCasesFromWebPage(url)
	whatToDoWithTestCase(testCases)


main(file)
