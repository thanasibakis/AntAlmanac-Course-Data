#!/usr/bin/env python3
#
# Description: a library of functions to analyze a dataset with columns: CourseCode, Data, Maximum, Enrolled, Requested, Waitlist
#
# Author: Thanasi Bakis
# Last Modified: 3/26/19

import pandas as pd

# Returns the first date that the class filled, or None
def whenDidClassFill(df, coursecode):
	dates = df[ (df.CourseCode == coursecode)
		 & (df.Maximum > 0)
		 & (df.Maximum == df.Enrolled) ].Date.tolist()

	return dates[0] if dates else None

# Returns average absolute (ie. |dy|) change in enrollment between days (excluding zero-change days)
def getAverageChangeInEnrollment(df, coursecode):
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
def whenDidEnrollmentChangeSignificantly(df, coursecode):
	avgChange = getAverageChangeInEnrollment(df, coursecode)
	data = df[ df.CourseCode == coursecode ]
	dates = df.Date.tolist()
	enrollmentCounts = data.Enrolled.tolist()

	lst = []

	for index in range(len(enrollmentCounts)):
		if index == len(enrollmentCounts) - 2:
			break

		if abs(enrollmentCounts[index + 1] - enrollmentCounts[index]) > avgChange:
			lst.append(dates[index + 1])

	return lst


# df = pd.read_csv("w18.txt.csv")