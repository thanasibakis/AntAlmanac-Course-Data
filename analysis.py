# Description: a library of functions to analyze course enrollment data
# Author: Thanasi Bakis

# Returns the dates that the class filled
def whenDidClassFill(df):

	allFullDates = df[ (df.Maximum > 0) & (df.Maximum == df.Enrolled) ].Date.tolist()

	if not allFullDates:
		return allFullDates

	fillDates = [allFullDates[0]]

	for index in range(len(allFullDates)):
		if index == len(allFullDates) - 1:
			break

		thisFillDate = allFullDates[index]
		nextFillDate = allFullDates[index + 1]
		thisEnrollment = df.Enrolled[df.Date == thisFillDate].values[0]
		nextEnrollment = df.Enrolled[df.Date == nextFillDate].values[0]

		# we only care about the first date in a sequence of consecutive full dates, the "fill date"
		# UNLESS the consecutive date was a full date for a raised enrollment cap
		if thisFillDate + 1 != nextFillDate or thisEnrollment != nextEnrollment:
			fillDates.append(allFullDates[index + 1])

	return fillDates

# Returns average increase (or decrease, if given as argument) in enrollment between days
def _getAverageChangeInEnrollment(df, decreasing):

	if decreasing:
		return df[(df.EnrollmentDifferences < 0)].EnrollmentDifferences.mean()
	else:
		return df[(df.EnrollmentDifferences > 0)].EnrollmentDifferences.mean()

# Returns a list of days that saw a larger-than-average jump (or drop, if given as argument)
def whenDidEnrollmentChangeSignificantly(df, decreasing):

	avgChange = _getAverageChangeInEnrollment(df, decreasing)

	if decreasing:
		# it likes to include day 0 here...
		return df[(df.EnrollmentDifferences < avgChange) & (df.Date != 0)].Date.tolist()

	else:
		return df[(df.EnrollmentDifferences > avgChange)].Date.tolist()

# Returns whether the class had a waitlist
def didWaitlistExist(df):

	return not df.Waitlist.isnull().any()

# Returns a list of days where the enrollment increased and the waitlist count decreased (we infer that the waitlist members became enrolled)
def whenDidWaitlistEnroll(df):

	return df[(df.EnrollmentDifferences > 0) & (df.WaitlistDifferences < 0)].Date.tolist()
