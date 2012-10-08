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


def processtree(repo,gitobjs):
	print "process tree";
	totalobjs=len(gitobjs);
	curobj=1;
	newtree = [];
	treefound = False;
	for gitobj in gitobjs:
		newobjs,newtreefound = processitem(repo,gitobj);
		treefound = treefound or newtreefound;
		print curobj," / ",totalobjs;
		curobj = curobj+1;
		print "added elements: ",len(newobjs);
		newtree.extend(newobjs);
	
	return newtree, treefound;

# Note that this function currently discards mode information.  Would be easy to add if we want to check file modes.
def processitem(repo,gitobj):
	objtype,name,objid,time,author,message = gitobj;

	if objtype=="blob":
		newobjs=[gitobj];
		treefound=False;
		print "blob ",newobjs
	else:
		newobjs=[];
		treefound=True;
		os.chdir(repo);
		output = subprocess.check_output(["git","ls-tree",objid]);
		for line in output.split("\n"):
			if len(line) > 0:
				mode, objtype, objelement = line.split(" ",3);
				objid, elementname = objelement.split("\t",1);
				if objtype=="tree":
					elementsep="/";
				else:
					elementsep="";
				elementname = name+elementname+elementsep;
				newobj=objtype,elementname,objid,time,author,message;
				newobjs.append(newobj);

	return newobjs, treefound


gitobjs = parsetree(repo);

treefound = True;
while treefound:
	print "total tree length: ",len(gitobjs);
	gitobjs,treefound = processtree(repo,gitobjs);

print "Final tree length: ",len(gitobjs);













#with open('/sstorage3/tmp/outfile.csv', 'wb') as outcsv:
#	outfile = csv.writer(outcsv);
#	outfile.writerows(gitobjs);

