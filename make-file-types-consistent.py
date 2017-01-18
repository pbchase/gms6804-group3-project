#!/usr/local/bin/python

# Make file types consistent

import magic
import os

path = "23andmedata/raw"
dirs = os.listdir(path)

for file in dirs:
	mypath = os.path.join(path,file)
	print mypath
	print magic.from_file(mypath)

