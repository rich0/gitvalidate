#!/usr/bin/python
# -*- coding: utf8 -*-

# Copyright 2012, Richard Freeman - See COPYING/README for license details.

import sys;
import os;
import subprocess;
import csv;

repo = '/home/rich/sstore3/gentoo-gitmig/git/gentoo-x86/'
head = 'c353557f65c845fd25ddda3b0ea9065be77c4a20'

def oldparsecommit(repo,commit):
	os.chdir(repo);
	output = subprocess.check_output(["git","cat-file","commit",commit]);

	message = "";

	for line in output.split("\n"):
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

	gitobject = "tree","",tree,time,tz,author,message
	return parent,gitobject

def oldparsetree(repo,head):
	parent = head;
	gitobjs = [];
	while parent != "":
		parent, info = parsecommit(repo, parent);
		gitobjs.append(info);

	return gitobjs;



def parsetree(repo):
	os.chdir(repo);
	gitobjs=[];

	output = subprocess.check_output(["git","log","--pretty=raw"]);

	message = "";
	skip1=True

	for line in output.split("\n"):
		if line.startswith("commit ") and not skip1:
			gitobject = "tree","",tree,time,author,message;
			gitobjs.append(gitobject);
			message="";
		elif line.startswith("commit "):
			skip1=False;
		elif len(message) > 0:
			message = message + "\n" + line;
		elif line.startswith("tree"):
			dummy, tree = line.split();
		elif line.startswith("parent"):
			pass;
		elif line.startswith("author"):
			dummy, right = line.split(" ",1);
			author, time, tz = right.rsplit(" ",2);
		elif line.startswith("committer"):
			pass;
		elif (len(line) > 0) and (len(message) == 0):
			message = line;


	gitobject = "tree","",tree,time,author,message
	gitobjs.append(gitobject);

	return gitobjs


gitobjs = parsetree(repo);


















#with open('/sstorage3/tmp/outfile.csv', 'wb') as outcsv:
#	outfile = csv.writer(outcsv);
#	outfile.writerows(gitobjs);

