#!/usr/bin/env python3
#
# Usage: ./txt_to_csv.py [filename]
# Output: [filename].csv is a long-form dataset with columns: CourseCode, Date, Maximum, Enrolled, Requested, Waitlist
# Author: Thanasi Bakis

import sys

oldfile = open(sys.argv[1], 'r')
newfile = open(f"{sys.argv[1]}.csv", 'w')

newfile.write("CourseCode,Date,Maximum,Enrolled,Requested,Waitlist\n")

while True:
	coursecode = oldfile.readline().strip()

	if coursecode == "=====":
		break

	# read lines into lists
	lineToList = lambda line: line.split(' ') if line != "n/a" else ['' for _ in range(38)]  # 38 dates
	maximum, enrolled, requested, waitlist = [ lineToList(oldfile.readline().strip()) for _ in range(4) ]

	dateCodes = map(str, range(38))  # encode dates M8, T8, ... as 0, 1, 2, ... to give them unique and ordered IDs
	entries = zip(dateCodes, maximum, enrolled, requested, waitlist)

	for entry in entries:
		line = ','.join( (coursecode,) + entry )
		newfile.write(line + "\n")

oldfile.close()
newfile.close()
