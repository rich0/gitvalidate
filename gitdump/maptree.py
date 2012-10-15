#!/usr/bin/python
# -*- coding: utf8 -*-

# Copyright 2012, Richard Freeman - See COPYING/README for license details.

import csv;
import base64;
import StringIO;
import sys;
from operator import itemgetter, attrgetter;
from pygit2 import Repository,GIT_OBJ_TREE;

repo = '/data/git/gentoo-x86/'
head = 'c353557f65c845fd25ddda3b0ea9065be77c4a20'

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

    for row in csv.reader([value]):
    	filename,filetype,filehash,filetime,author,message = row;
	if filetype=="blob":
		print '%s\t%s' % (filename, row)
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

			newrow=elementname,objtype,objid,filetime,author,message

			print '%s\t%s' % (elementname, csv2string(newrow));


# test framework
inline=",tree,5789de7076bfc534787fb3b072652810ca1ad197,1338260214,SmVmZiBIb3JlbGljayA8amRob3JlQGdlbnRvby5vcmc+,bWFya2VkIHg4NiBwZXIgYnVnIDQxNTM5MwoKKFBvcnRhZ2UgdmVyc2lvbjogMi4yLjBfYWxwaGExMDgvY3ZzL0xpbnV4IGk2ODYsIHVuc2lnbmVkIE1hbmlmZXN0IGNvbW1pdCkK"

redlines=[",tree,5789de7076bfc534787fb3b072652810ca1ad197,1338260214,SmVmZiBIb3JlbGljayA8amRob3JlQGdlbnRvby5vcmc+,bWFya2VkIHg4NiBwZXIgYnVnIDQxNTM5MwoKKFBvcnRhZ2UgdmVyc2lvbjogMi4yLjBfYWxwaGExMDgvY3ZzL0xpbnV4IGk2ODYsIHVuc2lnbmVkIE1hbmlmZXN0IGNvbW1pdCkK",",tree,5931a3b2eee2528e9f51204f8e1ef5e0ca150ce4,1338260203,SmVmZiBIb3JlbGljayA8amRob3JlQGdlbnRvby5vcmc+,bWFya2VkIHg4NiBwZXIgYnVnIDQxNTM5MwoKKFBvcnRhZ2UgdmVyc2lvbjogMi4yLjBfYWxwaGExMDgvY3ZzL0xpbnV4IGk2ODYpCg==",",tree,a2f1b803ef2cc0756c157e952cd9fb922507ea36,1338260095,QW5kcmV5IEtpc2x5dWsgPHdlYXZlckBnZW50b28ub3JnPg==,dmVyc2lvbiBidW1wCgooUG9ydGFnZSB2ZXJzaW9uOiAyLjIuMF9hbHBoYTc0L2N2cy9MaW51eCB4ODZfNjQsIHNpZ25lZCBNYW5pZmVzdCBjb21taXQgd2l0aCBrZXkgMTZFN0Q4RTYpCg=="];

if False:
	for key,value in mapper(0,inline):
		print "key= ",key
		print "value= ",value

if False:
	for key,value in reducer("asdf",redlines):
		print "key= ",key
		print "value= ",value


if False:
	if __name__ == "__main__":
	    import dumbo
	    dumbo.run(mapper, reducer, combiner=reducer)


