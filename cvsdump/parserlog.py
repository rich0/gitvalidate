#!/usr/bin/python
# -*- coding: utf8 -*-

# Copyright 2012, Richard Freeman - See COPYING/README for license details.

# Convert input rlog to:
# filename (utf8)
# revision
# filetime (unix timecode)
# author (utf8+base64)
# message (utf8+base64)

# Expects rlog format from rlog -z+00:00
# rlog must be run from repository root so all paths relative with ./ prepended to path - as in find | grep ",v" | xargs -n 1 rlog -z+00:00

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
from dateutil import tz;
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
			if subline.strip()==delim2 and filetime:
				newrow=filename.encode('utf-8'),filetime,base64.b64encode(author.encode('utf-8')),base64.b64encode(message.strip()),revision,state;
				outfile.writerow(newrow);

				startmessage=False
				message=""
			elif startmessage:
				if len(message)>0:
					sep="\n"
				else:
					sep=""
				message=message+sep+subline;
			elif subline.startswith("RCS file: "):
				filename=subline[10:].strip();
				filename=filename.replace("Attic/","")
				filename=filename[2:len(filename)-2]
			elif subline.startswith("revision "):
				revision=subline[9:].strip()
			elif subline.startswith("date: "):
				dummy,date,filetime,dummy2,dummy2a,author,dummy3,dummy3a,state=subline.split(" ",8)
				filetime,timez = filetime.split("+")
				state= state[:state.find(";")];
				timez=timez[:len(timez)-1]
				author=author[:len(author)-1]
				interimtime=iso8601.parse_date(date+" "+filetime+timez)
				interimtime = interimtime.astimezone(tz.tzlocal())
				interimtime = interimtime.timetuple()
				filetime=time.mktime(interimtime);
				startmessage=True;


		
		newrow=filename.encode('utf-8'),filetime,base64.b64encode(author.encode('utf-8')),base64.b64encode(message.strip()),revision,state;
		outfile.writerow(newrow);


		section=[]
	else:
		section.append(line);








