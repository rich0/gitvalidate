#!/usr/bin/python
# -*- coding: utf8 -*-

# Copyright 2012, Richard Freeman - See COPYING/README for license details.

import sys;
import os;
import subprocess;
import csv;
from operator import itemgetter, attrgetter;
from pygit2 import Repository,GIT_OBJ_TREE;

repo = '/home/rich/sstore3/gentoo-gitmig/git/gentoo-x86/'
head = 'c353557f65c845fd25ddda3b0ea9065be77c4a20'

depth = sys.argv[1];

def parsetreedirect(repo,depth):
	os.chdir(repo);
	gitobjs=[];
	
	depthpar="-"+depth;
	output = subprocess.check_output(["git","log","--pretty=raw",depthpar]);

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
			message = message + "\n" + line[4:];
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
			message = line[4:];

	gitobject = "tree","",tree,time,author,message
	gitobjs.append(gitobject);

	return gitobjs

def parsetreepygit(repo,depth):
	repository=Repository(repo);
	gitobjs=[];
	
	current = repository.head;
	currentdepth=0;
	depth=int(depth);

	while currentdepth<depth:
		message=current.message;
		tree=current.tree.hex;
		author=current.author.name+" <"+current.author.email+">";
		time=current.author.time;
		gitobject="tree","",tree,time,author,message
		gitobjs.append(gitobject);
		if len(current.parents)>0:
			current=current.parents[0];
		else:
			break;
		currentdepth=currentdepth+1;


	return gitobjs


def processtree(repo,gitobjs):
	newtree = [];
	treefound = False;
	for gitobj in gitobjs:
		newobjs,newtreefound = processitempygit(repo,gitobj);
		treefound = treefound or newtreefound;
		newtree.extend(newobjs);
	
	return newtree, treefound;

# Note that this function currently discards mode information.  Would be easy to add if we want to check file modes.
def processitemdirect(repo,gitobj):
	objtype,name,objid,time,author,message = gitobj;

	if objtype=="blob":
		newobjs=[gitobj];
		treefound=False;
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


# Note that this function currently discards mode information.  Would be easy to add if we want to check file modes.
def processitempygit(repo,gitobj):
	objtype,name,objid,time,author,message = gitobj;

	if objtype=="blob":
		newobjs=[gitobj];
		treefound=False;
	else:
		newobjs=[];
		treefound=True;
		
		repository=Repository(repo);
		tree=repository[objid];
#		tree=repository.lookup_reference(objid);
		for entry in tree:
			objtype=repository[entry.oid].type;
			if objtype==GIT_OBJ_TREE:
				objtype="tree";
			else:
				objtype="blob";
			objid=entry.hex;
			elementname=entry.name;

			if objtype=="tree":
				elementsep="/";
			else:
				elementsep="";
			elementname = name+elementname+elementsep;
			newobj=objtype,elementname,objid,time,author,message;
			newobjs.append(newobj);

	return newobjs, treefound



def prunetree(gitobjs):
	print "prune tree start ",len(gitobjs);	
	gitobjs=sorted(gitobjs, key=itemgetter(1,3));
	print "sort done";
	
	newgitobjs=[];
	firstitem=True;
	while len(gitobjs) > 0:
		if not firstitem:
			nextitem = gitobjs.pop();			
			if nextitem[2] != lastitem[2]:
				newgitobjs.append(lastitem);		
			lastitem=nextitem;
		else:
			firstitem=False;
			lastitem = gitobjs.pop();
	newgitobjs.append(lastitem);



	print "prune tree finish ",len(newgitobjs);
	return newgitobjs

gitobjs = parsetreepygit(repo,depth);

if True:
	treefound = True;
	while treefound:
		print "total tree length: ",len(gitobjs);
		gitobjs,treefound = processtree(repo,gitobjs);
		gitobjs=prunetree(gitobjs);


	print "Final tree length: ",len(gitobjs);



with open('/sstorage3/tmp/outfile.csv', 'wb') as outcsv:
	outfile = csv.writer(outcsv);
	for row in gitobjs:
		r0,r1,r2,r3,r4,r5 = row;
		r2=r2.encode('utf-8');
		r4=r4.encode('utf-8');
		r5=r5.encode('utf-8');
		newrow=r0,r1,r2,r3,r4,r5;
		outfile.writerow(newrow);

