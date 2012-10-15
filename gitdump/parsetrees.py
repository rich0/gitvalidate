#!/usr/bin/python
# -*- coding: utf8 -*-

# Copyright 2012, Richard Freeman - See COPYING/README for license details.

import sys;
import csv;
import base64;
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

#outcsv=open('/sstorage3/tmp/outfile.csv', 'wb');
outfile=csv.writer(sys.stdout);

while currentdepth<depth:
	message=base64.b64encode(current.message.encode('utf-8'));
	tree=current.tree.hex.encode('utf-8');
	author=current.author.name+" <"+current.author.email+">";
	author=base64.b64encode(author.encode('utf-8'));
	time=current.author.time;
	gitobject="","tree",tree,time,author,message
	outfile.writerow(gitobject);
	if len(current.parents)>0:
		current=current.parents[0];
	else:
		break;
	currentdepth=currentdepth+1;

