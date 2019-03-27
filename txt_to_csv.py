#!/usr/bin/env python3
#
# Usage: ./txt_to_csv.py [filename]
# Output: filename.csv is a long-form dataset with columns: CourseCode, Data, Maximum, Enrolled, Requested, Waitlist
#
# Author: Thanasi Bakis
# Last Modified: 3/26/19

import sys

dates = ("M8", "T8", "W8", "T8", "F8", "S8", "S8", "M9", "T9", "W9", "T9", "F9", "S9", "S9", "MT", "TT", "WT", "TT", "FT", "ST", "ST", "Mf", "Tf", "Wf", "Tf", "Ff", "M1", "T1", "W1", "T1", "F1", "S1", "S1", "M2", "T2", "W2", "T2", "F2")

oldfile = open(sys.argv[1], 'r')
newfile = open(f"{sys.argv[1]}.csv", 'w')

newfile.write("CourseCode,Date,Maximum,Enrolled,Requested,Waitlist\n")

while True:
	coursecode = oldfile.readline().strip()

	if coursecode == "=====":
		break

	# read lines into lists
	lineToList = lambda line: line.split(' ') if line != "n/a" else ['' for _ in dates]
	maximum, enrolled, requested, waitlist = [ lineToList(oldfile.readline().strip()) for _ in range(4) ]

	entries = zip(dates, maximum, enrolled, requested, waitlist)

	for entry in entries:
		line = ','.join( (coursecode,) + entry )
		newfile.write(line + "\n")

oldfile.close()
newfile.close()
