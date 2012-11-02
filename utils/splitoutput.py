#!/usr/bin/python
# -*- coding: utf8 -*-

# Copyright 2012, Richard Freeman - See COPYING/README for license details.
# Splits input at lines where first csv field changes

import sys;

lastkey=""

for line in sys.stdin:
    line=line.strip();
    key,dummy = line.split(",",1);
    if key!=lastkey:
        print
    print line
    lastkey=key
