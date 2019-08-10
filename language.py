# Description: a library of functions to textually describe courses
# Author: Thanasi Bakis

import analysis, Date

# Returns a human-readable summary of the course's enrollment trends in the given quarter's data frame.
def getEnrollmentDescription(df, coursecode):

	df = df[df.CourseCode == coursecode]

	fillDates = analysis.whenDidClassFill(df)
	increaseDates = analysis.whenDidEnrollmentChangeSignificantly(df, decreasing=False)
	decreaseDates = analysis.whenDidEnrollmentChangeSignificantly(df, decreasing=True)

	desc = _formDateSentence("This course", "filled", fillDates) + \
            _formDateSentence("Enrollment", "saw significant increases", increaseDates) + \
            _formDateSentence("It", "saw significant decreases", decreaseDates)

	if analysis.didWaitlistExist(df):
		desc += _formDateSentence("Waitlist members likely", "became enrolled", analysis.whenDidWaitlistEnroll(df))

	else:
		desc += "There was no waitlist for this course.\n"

	return desc.strip()


# Returns a sentences of the form "[subject] (never?) [verb] [dates]" because this structure shows up a lot
def _formDateSentence(subjectPhase, verbPhrase, dates: [Date]):
	return subjectPhase + ' ' + \
            ("never " if not dates else '') + \
            verbPhrase + \
            (' ' + _datesAsOnePhrase(dates) if dates else '') + ".\n"


# Combines "Monday of week 10" and "Tuesday of week 10" into "Monday and Tuesday of week 10"
def _datesAsOnePhrase(dates: [Date]):
    if not dates:
        return None

    pairs = [str(date).split(" of ") for date in dates]
    numUniqueWeeks = len({pair[1] for pair in pairs})

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

    string = "; ".join([" of ".join(pair) for pair in pairs])
    string = "; and ".join(string.rsplit("; ", 1))

    if ',' not in string:
    	string = string.replace(';', ',')

    if string.count(',') == 1:
    	string = string.replace(',', '')

    return string
