#!/usr/bin/python
# -*- coding: utf8 -*-

# Copyright 2012, Richard Freeman - See COPYING/README for license details.

import sys;
import csv;
import base64;
from pygit2 import Repository;

repo = sys.argv[1]  # '/data/gentoo-x86/'
head = sys.argv[2] # 'c353557f65c845fd25ddda3b0ea9065be77c4a20'

depth = sys.argv[3];

#rewrite this former function to just write each line to csv rather than forming a list

repository=Repository(repo);

current = repository.head;
currentdepth=0;
depth=int(depth);

#outcsv=open('/sstorage3/tmp/outfile.csv', 'wb');
outfile=csv.writer(sys.stdout);

while currentdepth<depth:
    newmessage=""
    for line in current.message.split("\n"):
        if line.startswith("RepoMan-Options") or line.startswith("Package-Manager") or line.startswith("Manifest-Sign-Key"):
            pass
        else:
            newmessage=newmessage+line+"\n";
    newmessage=newmessage.strip();    
    message=base64.b64encode(newmessage.encode('utf-8'))
    tree=current.tree.hex.encode('utf-8');
    commit=current.hex.encode('utf-8')
    author=current.author.name+" <"+current.author.email+">";
    author=base64.b64encode(author.encode('utf-8'));
    time=current.author.time;
    gitobject="","tree",tree,time,author,message,commit
    outfile.writerow(gitobject);
    if len(current.parents)>0:
        current=current.parents[0];
    else:
        break;
    currentdepth=currentdepth+1;
