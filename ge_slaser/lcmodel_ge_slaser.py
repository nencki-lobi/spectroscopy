#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import re
import shutil
from shutil import copyfile

#file pattern
pattern = '.*sLASER.*7$'
directory = sys.argv[1]

# wybranie odpowiedniego basis-seta w zalenosci od czasu echa (TE) w metodzie
# basis_set_dir = '/home/jorzel/.lcmodel/basis-sets/siemens-15t/gamma_press_te30_64mhz_088.basis'
#basis_set_dir = '/home/jorzel/.lcmodel/basis-sets/ge/press_te35_3t_gsh_v3.basis'
basis_set_dir = '/media/skorpion/badania/CNS/lcmodel/slaser.basis'

#basis_set_dir = '/home/jorzel/.lcmodel/basis-sets/ge/gamma_press_te288_128mhz_662d.basis'
#basis_set_dir = '/home/jorzel/.lcmodel/basis-sets/ge/gamma_press_te144_128mhz_648d.basis'
#wyszukiwanie folderow zawierajacych plik 'fid.refscan'
fileList = []
for root, subFolders, files in os.walk(directory):
	for file in files:
		if re.search(pattern,file):
			fileList.append(os.path.join(root,file))
items = len(fileList)
print('Number of files: %d' % items)
print(fileList)

for root in fileList:

	path, file_name = os.path.split(root)
	#path, name = os.path.split(path)
	name , ext = str.split(file_name,'.')

	print(path)
	print(name)

	if not os.path.exists(path+'/'):
		os.mkdir(path+'/')
	if not os.path.exists(path+'/'+name+'/'):
		os.mkdir(path+'/'+name+'/')
	if not os.path.exists(path+'/'+name+ '/h2o/'):
		os.mkdir(path+'/'+name+'/h2o/')
	if not os.path.exists(path+'/'+name +'/met/'):
		os.mkdir(path+'/'+name + '/met/')

	convert_bin2raw = ('/home/bkossows/.lcmodel/gelx/bin2raw ' +root+' '+path+'/'+name+'/ met')
	#convert_bin2raw = ('/home/jorzel/.lcmodel/siemens/bin2raw ' +root+' '+path+'/'+name+'/'+' met')
	os.system(convert_bin2raw)
	print(convert_bin2raw)
	print('Conversion left %d' % items)
	items -= 1

	shutil.copy(path+'/'+name+'/met/cpStart', path+'/'+name+'/met/myControl')

	zrodlo = open(path+'/'+name+'/met/myControl').readlines()
	cel = open(path+'/'+name+'/met/myControl', 'w')
	for s in zrodlo:
		cel.write(s.replace("title", "\ntitle"))
	cel.close()

	zrodlo = open(path+'/'+name+'/met/myControl').readlines()
	size_zrodlo = len(zrodlo)
	cel = open(path+'/'+name+'/met/myControl', 'w')
	for s,line in enumerate(zrodlo):
		if s==0:
			cel.write("$LCMODL\n")
		elif s==(size_zrodlo-1):
			print(zrodlo[s])
			cel.write(zrodlo[s]+'\n$END\n')
		else:
			cel.write(line)
	cel.close()

	if os.path.exists(path+'/'+name+'/h2o/RAW'):
		water_path = (path+'/'+name+'/h2o/RAW')
	csv_path = (path+'/'+name+'/spreadsheet.csv')
	table_path = (path+'/'+name+'/table')
	coord_path = (path+'/'+name+'/coord')

	zrodlo = open(path+'/'+name+'/met/myControl').readlines()
	cel = open(path+'/'+name+'/met/myControl', 'w')
	for s in zrodlo:
		cel.write(s.replace("$LCMODL", "$LCMODL\nfilbas= '"+basis_set_dir+"'\n"))
	cel.close()


	if os.path.exists(path+'/'+name+'/h2o/RAW'):
		zrodlo = open(path+'/'+name+'/met/myControl').readlines()
		cel = open(path+'/'+name+'/met/myControl', 'w')
		for s in zrodlo:
			cel.write(s.replace(basis_set_dir+"'", basis_set_dir+"'\nfilh2o= '" +water_path+"'\nfilcsv= '"+csv_path+"'\nfiltab= '"+table_path+"'\nfilcoo = '"+coord_path+"'"))
		cel.close()
	else:
		zrodlo = open(path+'/'+name+'/met/myControl').readlines()
		cel = open(path+'/'+name+'/met/myControl', 'w')
		for s in zrodlo:
			cel.write(s.replace(basis_set_dir+"'", basis_set_dir+"'\nfilcsv= '"+csv_path+"'\nfiltab= '"+table_path+"'\nfilcoo= '"+coord_path+"'"))
		cel.close()


	if os.path.exists(path+'/'+name+'/h2o/RAW'):
		zrodlo = open(path+'/'+name+'/met/myControl').readlines()
		cel = open(path+'/'+name+'/met/myControl', 'w')
		for s in zrodlo:
			cel.write(s.replace("doecc= T", "doecc=T\nneach=99\ndows=T\nlcsv=11\nltable=7\nlcoord=9\n$END"))
		cel.close()
	else:
		zrodlo = open(path+'/'+name+'/met/myControl').readlines()
		cel = open(path+'/'+name+'/met/myControl', 'w')
		for s in zrodlo:
			cel.write(s.replace("doecc= T", "doecc=F\nneach=99\nnlcsv=11\nltable=7\nlcoord=9\n$END"))
		cel.close()

	command = ('/home/bkossows/.lcmodel/bin/lcmodel <' +path+'/'+name+'/met/myControl')
	print(command)
	os.system(command)

	command=('ps2pdf ' + os.path.join(path,name,'ps ') + os.path.join(path,name,'lcmodel.pdf'))
	os.system(command)
