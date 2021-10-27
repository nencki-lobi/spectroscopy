#!/usr/bin/python
# -*- coding: utf-8 -*- 
import os
import sys
import re
from shutil import copyfile
from Tkinter import Tk
from tkFileDialog import askdirectory
import csv
if len(sys.argv)>1:
	directory = str(sys.argv[1])
else:
	Tk().withdraw()
	directory = askdirectory(title='Select search path')
pattern = 'spreadsheet.csv$' 
fileList = []
for root, subFolders, files in os.walk(directory):  
	for file in files:
		if re.search(pattern,file):
			fileList.append(os.path.join(root,file))  
items = len(fileList)
fileList.sort()
print('csvpy will analyze ' + directory + ' containing ' + str(items) + ' csv(s).')

met = []
sd = []
for file in fileList:
	content = []
	content2 = []
	with open(file, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in spamreader:
			#content.append(', '.join(row[2:len(row):3]))
			content.append(', '.join(row[2:len(row):3]))
			content2.append(', '.join(row[3:len(row):3]))
		met.append(os.path.split(file)[-2] + ',' + content[1])
		sd.append(os.path.split(file)[-2] + ',' + content2[1])

m = open(os.path.join(directory,"met.csv"), "w")
s = open(os.path.join(directory,"sd.csv"), "w")
mets=content[1].count(',')+1
sds=content2[1].count(',')+1
print >>m, ('['+str(items)+' '+str(mets)+'],'+ content[0] + '\n' + '\n'.join(met))
print >>s, ('['+str(items)+' '+str(sds)+'],'+ content2[0] + '\n' + '\n'.join(sd))
m.close
s.close
