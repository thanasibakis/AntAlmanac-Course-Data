#!/usr/bin/env python3
#
# Description: a library of functions to analyze a dataset with columns: CourseCode, Data, Maximum, Enrolled, Requested, Waitlist
# Author: Thanasi Bakis

import pandas as pd

# Returns a human-readable summary of the course's enrollment trends in the given quarter.
def getClassDescription(quarter, coursecode):

	df = pd.read_csv(quarter + ".txt.csv")  # to be replaced with some kind of SQL access hopefully
	desc = ""

	fillDate = _whenDidClassFill(df, coursecode)
	desc += f"This course {'never ' if not fillDate else ''}filled{' ' + fillDate if fillDate else ''}. "

	jumpDates = _whenDidEnrollmentChangeSignificantly(df, coursecode)
	desc += f"Enrollment {'never ' if not jumpDates else ''}saw large changes{' ' + jumpDates if jumpDates else ''}."

	return desc

# Returns the first date that the class filled
def _whenDidClassFill(df, coursecode):

	dates = df[ (df.CourseCode == coursecode)
		 & (df.Maximum > 0)
		 & (df.Maximum == df.Enrolled) ].Date.tolist()

	return _dateCodeToText(dates[0]) if dates else None

# Returns average absolute (ie. |dy|) change in enrollment between days (excluding zero-change days)
def _getAverageChangeInEnrollment(df, coursecode):

	enrollmentCounts = df[ df.CourseCode == coursecode ].Enrolled.tolist()

	sum = 0
	count = 0

	for index in range(len(enrollmentCounts)):
		if index == len(enrollmentCounts) - 2:
			break

		if enrollmentCounts[index] == enrollmentCounts[index + 1]:
			continue

		sum += abs(enrollmentCounts[index + 1] - enrollmentCounts[index])
		count += 1

	return sum / count

# Returns a list of days that saw a larger-than-average jump or drop
def _whenDidEnrollmentChangeSignificantly(df, coursecode):

	avgChange = _getAverageChangeInEnrollment(df, coursecode)
	data = df[ df.CourseCode == coursecode ]
	dates = df.Date.tolist()
	enrollmentCounts = data.Enrolled.tolist()

	lst = []

	for index in range(len(enrollmentCounts)):
		if index == len(enrollmentCounts) - 2:
			break

		if abs(enrollmentCounts[index + 1] - enrollmentCounts[index]) > avgChange:
			lst.append(dates[index + 1])

	return _dateCodeListToText(lst) if lst else None

# Converts a date code (0, 1, 2) to something human-readable (mon wk 8, tues wk 8, ...)
def _dateCodeToText(dateCode):

	# DO NOT REORDER! date codes are the index of the date in this tuple
	return ("Monday of week 8", "Tuesday of week 8", "Wednesday of week 8", "Thursday of week 8", "Friday of week 8", "Saturday of week 8", "Sunday of week 8",
		 "Monday of week 9", "Tuesday of week 9", "Wednesday of week 9", "Thursday of week 9", "Friday of week 9", "Saturday of week 9", "Sunday of week 9",
		 "Monday of week 10", "Tuesday of week 10", "Wednesday of week 10", "Thursday of week 10", "Friday of week 10", "Saturday of week 10", "Sunday of week 10",
		 "Monday of finals week", "Tuesday of finals week", "Wednesday of finals week", "Thursday of finals week", "Friday of finals week",
		 "Monday of week 1", "Tuesday of week 1", "Wednesday of week 1", "Thursday of week 1", "Friday of week 1", "Saturday of week 1", "Sunday of week 1",
		 "Monday of week 2", "Tuesday of week 2", "Wednesday of week 2", "Thursday of week 2", "Friday of week 2")[dateCode]  # we don't talk about this ok

# Like _dateCodeToText for a list of date codes, but combines "Monday of week 10" and "Tuesday of week 10" into "Monday and Tuesday of week 10"
def _dateCodeListToText(dateCodes):
	
	pairs = [ _dateCodeToText(date).split(" of ") for date in dateCodes ]
	numUniqueWeeks = len({ pair[1] for pair in pairs })

	i = 0

	while len(pairs) != numUniqueWeeks and i+1 < len(pairs):
		if pairs[i][1] == pairs[i+1][1]:
			day1 = pairs[i][0]
			pairs[i+1][0] = day1 + ", " + pairs[i+1][0]
			pairs = pairs[:i] + pairs[i+1:]
		
		else:
			i += 1
	
	for pair in pairs:
		pair[0] = ", and ".join(pair[0].rsplit(", ", 1))

		if pair[0].count(',') == 1:
			pair[0] = pair[0].replace(',', '')
	
	string = "; ".join([ " of ".join(pair) for pair in pairs ])
	string = "; and ".join(string.rsplit("; ", 1))

	if ',' not in string:
		string = string.replace(';', ',')
	
	return string