#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import re
import shutil
from shutil import copyfile

#file pattern
pattern = '\.7'
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

        if os.path.exists(path+'/'+name+'/h2o/RAW'):
                water_path = (path+'/'+name+'/h2o/RAW')
        csv_path = (path+'/'+name+'/spreadsheet.csv')
        table_path = (path+'/'+name+'/table')
        coord_path = (path+'/'+name+'/coord')

        file_content = list()
        source = open(os.path.join(path,name,'met/myControl'), 'r')
        for line in source.readlines():
                file_content.append(line)
        file_content.insert(0, "$LCMODL\n")
        file_content.insert(len(file_content), "\n$END")
        file_content.insert(len(file_content)-1, "filbas= '"+basis_set_dir+"'\n")
        file_content.insert(len(file_content)-1, "filcsv= '"+csv_path+"'\n")
        file_content.insert(len(file_content)-1, "filtab= '"+table_path+"'\n")
        file_content.insert(len(file_content)-1, "filcoo= '"+coord_path+"'\n")
        if os.path.exists(os.path.join(path,name,'h2o/RAW')):
                file_content.insert(len(file_content)-1, "filh2o= '" +water_path+"'\n")
                file_content.insert(len(file_content)-1, "dows= T\n")
                file_content.insert(len(file_content)-1, "doecc= T\n")
        file_content.insert(len(file_content)-1, "lcsv= 11\n")
        file_content.insert(len(file_content)-1, "ltable= 7\n")
        file_content.insert(len(file_content)-1, "lcoord= 9\n")

        if os.path.isfile(os.path.join(path,name)+'wconc.txt'):
        	f = open(os.path.join(path,name)+'wconc.txt', 'r')
                wconc=f.read()
                f.close
                print("Volume corrected WCONC = " + wconc)
                file_content.insert(len(file_content)-1, "wconc= " + wconc + "\n")

        source.close()
	#print file_content

        content = open(os.path.join(path,name,'met/myControl'), 'w')
        for line in xrange(len(file_content)):
                content.write(file_content[line])
        content.close()

	command = ('/home/bkossows/.lcmodel/bin/lcmodel <' +path+'/'+name+'/met/myControl')
	print(command)
	os.system(command)

	command=('ps2pdf ' + os.path.join(path,name,'ps ') + os.path.join(path,name,'lcmodel.pdf'))
	os.system(command)
