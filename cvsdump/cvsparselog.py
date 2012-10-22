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
from operator import itemgetter, attrgetter;

def csv2string(data):
    si = StringIO.StringIO();
    cw = csv.writer(si);
    cw.writerow(data);
    return si.getvalue().strip('\r\n');


repo = '/home/rich/sstore3/gentoo-gitmig/cvs/root/'
delim1 = "=============================================================================" 
delim2 = "----------------------------"

outfile=csv.writer(sys.stdout);

section=[]
for line in sys.stdin:
	if line.strip() == delim1 and len(section)>0:
		startmessage=False;
		message=""
		filetime=0;
		for subline in section:
			if subline.startswith("Working file: "):
				filename=subline[14:].strip();
			elif subline.startswith("revision "):
				revision=subline[9:].strip()
			elif subline.startswith("date: "):
				dummy,date,filetime,tz,dummy2,dummy2a,author,dummy3,dummy3a,state=subline.split(" ",9)
				state= state[:state.find(";")];
				tz=tz[:len(tz)-1]
				author=author[:len(author)-1]
				filetime=time.mktime(iso8601.parse_date(date+" "+filetime+" "+tz).timetuple());
				startmessage=True;
			elif subline.strip()==delim2 and filetime:
				newrow=filename.encode('utf-8'),filetime,base64.b64encode(author.encode('utf-8')),base64.b64encode(message),revision,state;
				outfile.writerow(newrow);

				startmessage=False
				message=""
			elif startmessage:
				if len(message)>0:
					sep="\n"
				else:
					sep=""
				message=message+sep+subline;

		
		newrow=filename.encode('utf-8'),filetime,base64.b64encode(author.encode('utf-8')),base64.b64encode(message),revision,state;
		outfile.writerow(newrow);


		section=[]
	else:
		section.append(line);








