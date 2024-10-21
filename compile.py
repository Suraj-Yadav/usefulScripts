#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compiles the given Source Code.
"""

import argparse
import subprocess
from os import path, remove
from sys import platform


def compile(sourceFile, buildType="COMPILE"):
    (filePathWithoutExt, fileExtension) = path.splitext(sourceFile)

    command = []

    if fileExtension == ".cpp" or fileExtension == ".c":
        if platform.startswith("win32"):
            targetFile = filePathWithoutExt + ".exe"
        else:
            targetFile = filePathWithoutExt + ".out"

    if path.exists(targetFile):
        if (
            path.getmtime(sourceFile) >= path.getmtime(targetFile)
            or buildType != "COMPILE"
        ):
            remove(targetFile)
        else:
            exit(0)

    includeOptions = []
    linkerOptions = []
    flags = []
    if buildType == "COMPILE":
        flags += ["-O2"]
    elif buildType == "DEBUG":
        flags += ["-g"]
    elif buildType == "PROFILE":
        flags += ["-O2", "-pg"]
    flags += ["-std=c++17", "-Wpedantic", "-Wextra", "-Wall", "-Wshadow"]

    command = ["g++", "-o", targetFile]
    command += flags
    command += includeOptions
    command += [sourceFile]
    command += linkerOptions

    print(*command)
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )

    print(result.stdout)
    print(result.stderr)


def allowedFiles(choices):
    def CheckExt(choices, fileName):
        if not path.isfile(fileName):
            raise argparse.ArgumentTypeError(
                f'File "{fileName}" doesn\'t Exist',
            )
        ext = path.splitext(fileName)[1][1:]
        if ext not in choices:
            raise argparse.ArgumentTypeError(
                "Only {} files are supported".format(choices)
            )
        return fileName

    return lambda fileName: CheckExt(choices, fileName)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        "file",
        type=allowedFiles({"cpp", "c"}),
        help="Source File to Compile",
    )

    parser.add_argument(
        "buildType",
        default="COMPILE",
        nargs="?",
        choices=["COMPILE", "DEBUG", "PROFILE"],
        help="Type of Build. Only applicable for C/C++ files, ignored otherwise",
    )
    args = parser.parse_args()

    compile(args.file, args.buildType)
