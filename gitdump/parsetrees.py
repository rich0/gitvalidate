#!/usr/bin/python
# -*- coding: utf8 -*-

# Copyright 2012, Richard Freeman - See COPYING/README for license details.

import sys;
import os;
import subprocess;
import csv;
import multiprocessing;
import itertools;
from operator import itemgetter, attrgetter;
from pygit2 import Repository,GIT_OBJ_TREE;

repo = '/home/rich/sstore3/gentoo-gitmig/git/gentoo-x86/'
head = 'c353557f65c845fd25ddda3b0ea9065be77c4a20'

depth = sys.argv[1];

#rewrite this former function to just write each line to csv rather than forming a list

repository=Repository(repo);

current = repository.head;
currentdepth=0;
depth=int(depth);

outcsv=open('/sstorage3/tmp/outfile.csv', 'wb');
outfile=csv.writer(outcsv);

while currentdepth<depth:
	message=current.message.encode('utf-8');
	tree=current.tree.hex.encode('utf-8');
	author=current.author.name+" <"+current.author.email+">";
	author=author.encode('utf-8');
	time=current.author.time;
	gitobject="tree","",tree,time,author,message
	outfile.writerow(gitobject);
	if len(current.parents)>0:
		current=current.parents[0];
	else:
		break;
	currentdepth=currentdepth+1;



if False:
	with open('/sstorage3/tmp/outfile.csv', 'wb') as outcsv:
		outfile = csv.writer(outcsv);
		for row in gitobjs:
			r0,r1,r2,r3,r4,r5 = row;
			r2=r2.encode('utf-8');
			r4=r4.encode('utf-8');
			r5=r5.encode('utf-8');
			newrow=r0,r1,r2,r3,r4,r5;
			outfile.writerow(newrow);

if False:
	newobjs=[];
	with open('/sstorage3/tmp/outfile.csv','rb') as incsv:
		infile=csv.reader(incsv);
		for row in infile:
			r0,r1,r2,r3,r4,r5 = row;
			r2=r2.decode('utf-8');
			r3=int(r3);
			r4=r4.decode('utf-8');
			r5=r5.decode('utf-8');
			newrow=r0,r1,r2,r3,r4,r5;	
			newobjs.append(newrow);
	print gitobjs==newobjs;

