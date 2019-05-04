#!/usr/bin/env python3
#
# Description: a library of functions to analyze a dataset with columns: CourseCode, Date, Maximum, Enrolled, Waitlist
# Author: Thanasi Bakis

import pandas as pd
import sys

# Returns a human-readable summary of the course's enrollment trends in the given quarter's data frame.
def getClassDescription(coursecode, df):

	df = df[ df.CourseCode == coursecode ]
	desc = ""

	fillDates = _dateCodeListToText(_whenDidClassFill(df))
	desc += _formSentence("This course", "filled", fillDates)

	increaseDates = _dateCodeListToText(_whenDidEnrollmentChangeSignificantly(df, decreasing = False))
	desc += _formSentence("Enrollment", "saw significant increases", increaseDates)

	decreaseDates = _dateCodeListToText(_whenDidEnrollmentChangeSignificantly(df, decreasing = True))
	desc += _formSentence("It", "saw significant decreases", decreaseDates)

	if _didWaitlistExist(df):
		waitlistEnrollDates = _dateCodeListToText(_whenDidWaitlistEnroll(df))
		desc += _formSentence("Waitlist members likely", "became enrolled", waitlistEnrollDates)
	
	else:
		desc += "There was no waitlist for this course.\n"

	return desc.strip()

# Returns a sentences of the form "[subject] (never?) [verb] [dates]" because this structure shows up a lot
def _formSentence(subjectPhase, verbPhrase, datesText):
	return subjectPhase + ' ' + ("never " if not datesText else '') + verbPhrase + (' ' + datesText if datesText else '') + ".\n"

# Retrieves the data frame for the given quarter
def _getQuarterDF(quarter):
	df = pd.read_csv(quarter + ".txt.csv")  # this could get changed to anything, once we change data storage
	
	df["EnrollmentDifferences"] = df.Enrolled.diff()  # we'll be needing these later
	df["WaitlistDifferences"] = df.Waitlist.diff()

	return df

# Returns the dates that the class filled
def _whenDidClassFill(df):

	allFullDates = df[ (df.Maximum > 0) & (df.Maximum == df.Enrolled) ].Date.tolist()

	if not allFullDates:
		return allFullDates
		
	fillDates = [ allFullDates[0] ]

	for index in range(len(allFullDates)):
		if index == len(allFullDates) - 1:
			break
		
		thisFillDate = allFullDates[index]
		nextFillDate = allFullDates[index + 1]
		thisEnrollment = df.Enrolled[ df.Date == thisFillDate ].values[0]
		nextEnrollment = df.Enrolled[ df.Date == nextFillDate ].values[0]
		
		# we only care about the first date in a sequence of consecutive full dates, the "fill date"
		# UNLESS the consecutive date was a full date for a raised enrollment cap
		if thisFillDate + 1 != nextFillDate or thisEnrollment != nextEnrollment:
			fillDates.append(allFullDates[index + 1])

	return fillDates

# Returns average increase (or decrease, if given as argument) in enrollment between days
def _getAverageChangeInEnrollment(df, decreasing):

	if decreasing:
		return df[ (df.EnrollmentDifferences < 0) ].EnrollmentDifferences.mean()
	else:
		return df[ (df.EnrollmentDifferences > 0) ].EnrollmentDifferences.mean()

# Returns a list of days that saw a larger-than-average jump (or drop, if given as argument)
def _whenDidEnrollmentChangeSignificantly(df, decreasing):

	avgChange = _getAverageChangeInEnrollment(df, decreasing)

	if decreasing:
		return df[ (df.EnrollmentDifferences < avgChange) & (df.Date != 0) ].Date.tolist()  # it likes to include day 0 here...
	
	else:
		return df[ (df.EnrollmentDifferences > avgChange) ].Date.tolist()

# Returns whether the class had a waitlist
def _didWaitlistExist(df):

	return not df.Waitlist.isnull().any()

# Returns a list of days where the enrollment increased and the waitlist count decreased (we infer that the waitlist members became enrolled)
def _whenDidWaitlistEnroll(df):

	return df[ (df.EnrollmentDifferences > 0) & (df.WaitlistDifferences < 0) ].Date.tolist()

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

	if not dateCodes:
		return dateCodes
	
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

	if string.count(',') == 1:
		string = string.replace(',', '')
	
	return string




# Get descriptions for all quarters listed in the shell call ( ./gendescriptions w18 s18 ... )
if __name__ == "__main__":

	def _exportDescription(coursecode, quarter, df):
		file = open(f"{quarter}/{coursecode}.txt", 'w')
		file.write(getClassDescription(coursecode, df))
		file.close()

	for quarter in sys.argv[1:]:
		print("Generating descriptions for " + quarter)
		df = _getQuarterDF(quarter)
		df.CourseCode.apply(lambda c: _exportDescription(c, quarter, df))
	
	print("All done.")