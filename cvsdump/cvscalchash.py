#!/usr/bin/python
# -*- coding: utf8 -*-

# Copyright 2012, Richard Freeman - See COPYING/README for license details.

# Convert input cvs log to:
# filename (utf8)
# revision
# filetime (unix timecode)
# author (utf8+base64)
# message (utf8+base64)

import sys;
import os;
import subprocess;
import csv;
import multiprocessing;
import itertools;
import datetime;
import time;
import base64;
import iso8601;
import hashlib;
from operator import itemgetter, attrgetter;

def csv2string(data):
    si = StringIO.StringIO();
    cw = csv.writer(si);
    cw.writerow(data);
    return si.getvalue().strip('\r\n');


repo = '/home/rich/sstore3/gentoo-gitmig/cvs/checkout/gentoo-x86/'
module = 'gentoo-x86/'

outfile=csv.writer(sys.stdout);
os.chdir(repo);

for line in sys.stdin:
	line=line.strip();
	if len(line) > 0:
		for row in csv.reader([line]):
#			print row;
			filename,filetime,author,message,revision,state = row
			if state != "dead":
				output=subprocess.check_output(["cvs","co","-p","-r",revision,module+filename]).split("\n")
				output='\n'.join(output)
				final="blob "+str(len(output))+"\x00"+output;
				filehash=hashlib.sha1(final).hexdigest();
				newrow=filename,"blob",filehash,filetime,author,message
				outfile.writerow(newrow)

