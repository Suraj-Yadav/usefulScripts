#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reads TestCases from the given File and runs the File on each Test Set
"""

import argparse
import difflib
import subprocess
from os import path
from sys import platform

from rich.console import Console
from rich.table import Table


def allowedFiles(choices):
    def CheckExt(choices, fileName):
        if not path.isfile(fileName):
            raise argparse.ArgumentTypeError(f'File "{fileName}" doesn\'t Exist')
        ext = path.splitext(fileName)[1][1:]
        if ext not in choices:
            raise argparse.ArgumentTypeError(f"Only {choices} type files are supported")
        return fileName

    return lambda fileName: CheckExt(choices, fileName)


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "file", type=allowedFiles({"py", "cpp", "c"}), help="Source File to Test"
)
file = parser.parse_args().file
filename, file_extension = path.splitext(file)

content = open(file).readlines()

has_test_cases = any(True for line in content if line == "/***\n")

if not has_test_cases:
    print(f"No TestCase found in file: {file}")
    exit()

if file_extension == ".py":
    command = ["python3", file]
elif file_extension == ".c" or file_extension == ".cpp":
    if platform.startswith("win32"):
        command = [filename + ".exe"]
    else:
        command = ["./" + filename + ".out"]

rows = []
totalTestCases = 0
passedTestCases = 0
failedTestCases = 0
ignoredTestCases = 0


def colorThis(string: str, color: str):
    return f"[{color}]{string}[/{color}]"


def run(input, expected):
    global totalTestCases, passedTestCases, failedTestCases, ignoredTestCases
    totalTestCases += 1
    p = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        universal_newlines=True,
    )

    try:
        o = p.communicate(input, timeout=5)
    except subprocess.TimeoutExpired:
        p.kill()
        o = ["TLE"]

    returnCode = p.returncode

    output = "\n".join(list(map(str.strip, o[0].split("\n"))))
    expected = "\n".join(list(map(str.strip, expected.split("\n"))))

    output = output.strip()
    expected = expected.strip()

    if returnCode == 0 and expected == "":
        ignoredTestCases += 1
        textColor = "white"
    elif returnCode == 0 and output == expected:
        passedTestCases += 1
        textColor = "green"
    else:
        failedTestCases += 1
        textColor = "red"

    diff = ""
    if textColor == "red":
        codes = difflib.SequenceMatcher(a=expected, b=output).get_opcodes()
        for code in codes:
            s = code[0]
            e = expected[code[1] : code[2]]
            o = output[code[3] : code[4]]
            if s == "equal":
                diff += colorThis(e, "white")
            elif s == "delete":
                diff += colorThis(e, "red")
            elif s == "insert":
                diff += colorThis(o, "green")
            elif s == "replace":
                diff += colorThis(e, "red") + colorThis(o, "green")

    if returnCode != 0:
        expected += f"\nreturned {returnCode}"

    rows.append(
        [
            colorThis(input.strip(), textColor),
            colorThis(expected, textColor),
            colorThis(output, textColor),
            diff,
        ]
    )


inTest = False
inInput = False
inOutput = False
input = ""
expected = ""
for line in content:
    if inTest:
        if "---" in line:
            inOutput = True
            inInput = False
        elif "***/" in line:
            run(input, expected)
            inTest = False
            inInput = False
            inOutput = False
            input = ""
            expected = ""
        elif inInput:
            input += line
        elif inOutput:
            expected += line
    else:
        if "/***" in line:
            inTest = True
            inInput = True


console = Console()

table = Table(
    show_header=True,
    header_style="bold magenta",
    show_lines=True,
)

table.add_column("Input")
table.add_column("Expected")
table.add_column("Actual")
table.add_column("Diff")

for row in rows:
    table.add_row(*row)

console.print(table)


if ignoredTestCases + passedTestCases == totalTestCases:
    console.print(f"[green]Passed {passedTestCases}/{totalTestCases}[/green]")
else:
    console.print(f"[red]Failed {failedTestCases}/{totalTestCases}[/red]")
