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
import iso8601;
from operator import itemgetter, attrgetter;

repo = '/home/rich/sstore3/gentoo-gitmig/cvs/root/'
delim1 = "=============================================================================" 
delim2 = "----------------------------"

section=[]
for line in sys.stdin:
	if line.strip() == delim1 and len(values)>0:
		startmessage=False;
		message=""
		for subline in section:
			if subline.startswith("Working file: "):
				filename=subline[14:]
			elif subline.startswith("revision "):
				revision=subline[9:]
			elif subline.startswith("date: "):
				dummy,date,time,tz,dummy2,author,dummy3,state,dummy4=subline.split(" ",8)
				tz=tz[:len(tz-1)]
				author=author[:len(author-1)]
				filetime=time.mktime(iso8601.parse_date(date+" "+time+" "+tz).timetuple());
				startmessage=True;
			elif subline==delim2:
				#dump the revision



# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


				startmessage=False
				message=""
			elif startmessage
				message=message+"\n"+subline;
			


		
	




		section=[]
	else:
		section.append(value);








