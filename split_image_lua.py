# !/usr/bin/python
# -*- coding: UTF-8 -*-

#Copyright:     
#File:          rewrite_file_lua.py
#Author:        Benny Wong
#Email:         
#Date:          2023-08-29
#Description:   拆分lua拼图

import sys
import os
import time
import re
from PIL import Image
import shutil

scripts_path = os.path.join(sys.path[0], '文件名.lua')

print "scripts path",scripts_path

def getListImageScripts(filePath, listFile):
    file = open(filePath, "rb")
    fileStr = file.read()
    file.close()

    fileStrList = re.findall(r'\[[^\[\}]+\}', fileStr)

    valueName = ""
    valueFile = ""
    valueX = ""
    valueY = ""
    valueW = ""
    valueH = ""
    valueRotated = ""
    for s in fileStrList:
        valueName = re.findall(r'\[\"[^\]]+\"\]', s)[0].replace("[\"", "").replace("\"]", "")
        valueFile = re.findall(r'file=[^\f\n\r\t\v,]+', s)[0].replace("file=", "").replace("\"", "")
        valueX = re.findall(r'x=[^ \f\n\r\t\v,]+', s)[0].replace("x=", "")
        valueY = re.findall(r'y=[^ \f\n\r\t\v,]+', s)[0].replace("y=", "")
        valueW = re.findall(r'width=[^ \f\n\r\t\v,]+', s)[0].replace("width=", "")
        valueH = re.findall(r'height=[^ \f\n\r\t\v,]+', s)[0].replace("height=", "")
        valueRotated = re.findall(r'rotated=[^ \f\n\r\t\v,]+', s)[0].replace("rotated=", "")

        item = {
            "name" : valueName,
            "x" : valueX,
            "y" : valueY,
            "w" : valueW,
            "h" : valueH,
            "rotated" : valueRotated,
        }

        if listFile.has_key(valueFile):
            listFile[valueFile].append(item)
        else:
            listFile[valueFile] = [item]

def getSplitImage(fileName, fileList):
    filePath = os.path.join(sys.path[0], fileName.replace(".png", ""))
    print("filePath", filePath)
    # if os.path.exists(filePath):
    #     shutil.rmtree(filePath)
    # else:
    #     os.mkdir(filePath)
    os.mkdir(filePath)

    srcImage = Image.open(os.path.join(sys.path[0], fileName))

    for file in fileList:
        fileX = int(file["x"])
        fileY = int(file["y"])
        fileW = int(file["w"])
        fileH = int(file["h"])

        srcRect = [fileX, fileY, fileX + fileW, fileY + fileH]

        destX = 0
        destY = 0
        destW = fileW
        destH = fileH

        destRect = [destX, destY, destX + destW, destY + destH]

        srcCrop = srcImage.crop(srcRect)

        destImage = Image.new("RGBA", [destW, destH])
        destImage.paste(srcCrop, destRect)
        if file["rotated"] == "true":
            destImage = destImage.transpose(Image.ROTATE_270)
        destImage.save(os.path.join(filePath, file["name"]))


# -------------- main --------------
if __name__ == '__main__':
    print "start", time.asctime(time.localtime(time.time()))
    
    listFileScripts = {}
    getListImageScripts(scripts_path, listFileScripts)

    for file in listFileScripts:
        getSplitImage(file, listFileScripts[file])

    print "end", time.asctime(time.localtime(time.time()))
    os.system("pause")