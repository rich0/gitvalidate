#!/usr/bin/python
# -*- coding: utf8 -*-

# Copyright 2012, Richard Freeman - See COPYING/README for license details.

import csv;
import sys;
import base64;
import StringIO;
from operator import itemgetter, attrgetter;
from pygit2 import Repository,GIT_OBJ_TREE;


# CSV input format:
# filename - utf8
# filetype - "blob" or "tree"
# filehash - utf8
# filetime - unix timecode
# author - utf8+base64
# message - utf8+base64

def csv2stringrows(data):
    si = StringIO.StringIO();
    cw = csv.writer(si);
    cw.writerows(data);
    return si.getvalue();

# reducer input: key=filename, values=collection of strings of all.  Output key=filename, value=all.

def reducevalues(values):
	# first convert values to list
	gitobjs=[];
	for row in csv.reader(values):
		gitobjs.append(row);

	gitobjs=sorted(gitobjs, key=itemgetter(0,3));
	newgitobjs=[];

	firstitem=True;
	while len(gitobjs) > 0:
		if not firstitem:
			nextitem=gitobjs.pop();
			if nextitem[2] != lastitem[2]:
				newgitobjs.append(lastitem);
			lastitem=nextitem;
		else:
			firstitem=False;
			lastitem=gitobjs.pop();
	newgitobjs.append(lastitem);

	print csv2stringrows(newgitobjs);



values=[];
lastkey="";
for line in sys.stdin:
	line=line.strip();
	value = line
	key,dummy = line.split(",",1);
	if key!=lastkey and len(values)>0:
		reducevalues(values)

		values=[];
		lastkey=key;
	else:
		lastkey=key;
	values.append(value);
reducevalues(values);

