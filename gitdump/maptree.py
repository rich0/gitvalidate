#!/usr/bin/python
# -*- coding: utf8 -*-

# Copyright 2012, Richard Freeman - See COPYING/README for license details.

import csv;
import StringIO;
import sys;
from pygit2 import Repository,GIT_OBJ_TREE;

repo = '/data/gentoo-x86/'

# CSV input format:
# filename - utf8
# filetype - "blob" or "tree"
# filehash - utf8
# filetime - unix timecode
# author - utf8+base64
# message - utf8+base64

def csv2string(data):
    si = StringIO.StringIO();
    cw = csv.writer(si);
    cw.writerow(data);
    return si.getvalue().strip('\r\n');

def csv2stringrows(data):
    si = StringIO.StringIO();
    cw = csv.writer(si);
    cw.writerows(data);
    return si.getvalue();

# mapper input: value = line.  Output key=filename, value=all
repository=Repository(repo);
for value in sys.stdin:
    value = value.strip();
    if len(value) > 0:
        for row in csv.reader([value]):
            filename,filetype,filehash,filetime,author,message,commit = row;
            if filetype.find("blob")!=-1:
                print '%s\t%s' % (filename,value)
            else:
                filehash=filehash.decode('utf-8');
                filename=filename.decode('utf-8');
                tree=repository[unicode(filehash)];
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
                    elementname = filename+elementname+elementsep;
                    
                    elementname = elementname.encode('utf-8');
                    objid = objid.encode('utf-8');
    
                    newrow=elementname,objtype,objid,filetime,author,message,commit
                    print '%s\t%s' % (elementname, csv2string(newrow));

