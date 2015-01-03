#!/usr/bin/python
# coding=utf-8

#Copyright:     
#File:          CreateFile.py
#Author:        Benny Huang
#Email:         harvyson@gmail.com
#Date:          2014-12-28
#Description:   

import os, sys, re, traceback
from datetime import datetime
from string import Template

def CreateFile_H(fileName, classHead, className):
    filePath = r"%s.h" % fileName
    
    classFile = open(filePath, "w")
    
    lines = []
    
    template_file = open(r"class_node_h.template", "r")
    template_obj = Template(template_file.read())
    
    lines.append(template_obj.substitute(
        FILE_NAME = fileName,
        GENE_DATA = datetime.now().strftime("%Y-%m-%d"),
        CLASS_HEAD = classHead,
        CLASS_NAME = className))
    
    classFile.writelines(lines)
    classFile.close()
    
def CreateFile_CPP(fileName, className):
    filePath = r"%s.cpp" % fileName
    
    classFile = open(filePath, "w")
    
    lines = []
    
    template_file = open(r"class_node_cpp.template", "r")
    template_obj = Template(template_file.read())
    
    lines.append(template_obj.substitute(
        FILE_NAME = fileName,
        GENE_DATA = datetime.now().strftime("%Y-%m-%d"),
        CLASS_NAME = className))
    
    classFile.writelines(lines)
    classFile.close()
    
def CreateClassFile():
    className = raw_input("ClassName: ")
    className = className.strip()

    fileName = className
    classHead = ""
    lastIndex = 0
    for i, ch in enumerate(className):
        if(not ch.islower() and i != 0):
            classHead += className[lastIndex : i].upper() + "_"
            lastIndex = i
    classHead += className[lastIndex:].upper()

    CreateFile_H(fileName, classHead, className)
    CreateFile_CPP(fileName, className)
    
# -------------- main --------------
if __name__ == '__main__':
    CreateClassFile()
    # os.system("pause")