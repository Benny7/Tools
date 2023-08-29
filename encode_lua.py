#!/usr/bin/python
# -*- coding: UTF-8 -*-

#File:          encode_lua.py
#Author:        Benny Wong
#Email:         
#Date:          2023-08-29
#Description:   脚本加密

import sys
import os
import time

scripts_path = os.path.join(sys.path[0], 'app', 'src', 'main', 'assets', 'scripts')
debug_path = os.path.join(sys.path[0], 'app', 'src', 'main', 'assets', 'scripts', 'debug_config.lua')

print "scripts path",scripts_path

def codeLua(path):
    file = open(path, "rb")
    fileStr = file.read()
    file.close()

    isDecode = fileStr.startswith("BYLUA")
    fileStrList = list(fileStr)
    keyStrList = list("boyaa")

    if isDecode:
        fileStrList = fileStrList[5:]

    for k, v in enumerate(fileStrList):
        temp = ord(fileStrList[k])
        temp = temp ^ ord(keyStrList[k % 5])
        fileStrList[k] = chr(temp)

    if not isDecode:
        fileStrList.insert(0, "BYLUA")

    result = "".join(fileStrList)

    file = open(path, "wb")
    file.write(result)
    file.close()

def code(src):
    print("code %s" % src)
    for root, subdirs, files in os.walk(src):
        for path in files:
            filePath = os.path.join(root, path)
            fileFormat = os.path.splitext(filePath)[-1]
            if fileFormat in [".lua"]:
                codeLua(filePath)

# -------------- main --------------
if __name__ == '__main__':
    if os.path.exists(debug_path):
        os.remove(debug_path)
        print "remove", debug_path

    print "code start", time.asctime(time.localtime(time.time()))
    code(scripts_path)
    print "code end", time.asctime(time.localtime(time.time()))
    os.system("pause")