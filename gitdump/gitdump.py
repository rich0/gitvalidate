#!/usr/bin/python
# -*- coding: utf8 -*-

# Copyright 2012, Richard Freeman - See COPYING/README for license details.

import sys;
import os;
import subprocess;

repo = '/home/rich/sstore3/gentoo-gitmig/git/gentoo-x86/'
head = 'c353557f65c845fd25ddda3b0ea9065be77c4a20'

def parsecommit(repo,commit):
	os.chdir(repo);
	output = subprocess.check_output(["git","cat-file","commit",commit]);
	print output;

	message = "";

	for line in output.split("\n"):
	   print line;
	   if len(message) > 0:
	      message = message + "\n" + line;
	   elif line.startswith("tree"):
	      dummy, tree = line.split();
	   elif line.startswith("parent"):
	      dummy, parent = line.split();
	   elif line.startswith("author"):
	      dummy, right = line.split(" ",1);
	      author, time, tz = right.rsplit(" ",2);
	   elif line.startswith("committer"):
	      dummy = "";
	   elif (len(line) > 0) and (len(message) == 0):
	      message = line;


	print tree, parent;
	print author;
	print time, tz;
	print message;

	gitobject = "tree","",tree,time,tz,author,message
	return parent,gitobject

parent, info = parsecommit(repo, head);
print "parent: ",parent;
objtype, name, hashdata, time, tz, author, message = info;
print info;

