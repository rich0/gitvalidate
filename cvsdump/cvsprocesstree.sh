#!/bin/bash
# Parameters:
# $1 - path to gentoo-x86 in cvs root (contains rcs files)
# $2 - path to cvs checkout of gentoo-x86

cd "$1"
find | grep ",v" | parallel cvslogparse.sh | parallel --pipe cvscalchash.py "$2" gentoo-x86/  | sort -t , -k 1,1 -k 2,2rn | csvreduce.py | sed '/^$/d'
