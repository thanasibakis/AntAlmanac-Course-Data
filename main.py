#!/usr/bin/env python3
#
# Description: a program to visualze & textually describe courses
# Author: Thanasi Bakis


import pandas as pd
import matplotlib.pyplot as plt
import language, visuals, sys
from Date import Date

EXPORT_DIR = "./data"


# Retrieves the data frame for the given quarter.
# Expects a dataset with columns: CourseCode, Date (as an integer date code), Maximum, Enrolled, Requested, Waitlist
# TODO: should verify the dataset has required columns
def getQuarterDF(quarter):
	
	df = pd.read_csv("../Data/" + quarter + ".txt.csv")  # this could get changed to anything, once we change data storage
	
	df["Date"] = df.Date.apply(Date) # turn date codes into Date objects
	df["EnrollmentDifferences"] = df.Enrolled.diff()  # we'll be needing these later
	df["WaitlistDifferences"] = df.Waitlist.diff()

	return df


# Writes the enrollment description for the given course to a file
def exportEnrollmentDescription(df, quarter_name, coursecode):
	
	file = open(f"{EXPORT_DIR}/{quarter_name}_{coursecode}_enrollment_description.txt", 'w')
	file.write(language.getEnrollmentDescription(df, coursecode))
	file.close()


# Writes the enrollment visual for the given course to a file
def exportEnrollmentVisual(df, quarter_name, coursecode):

	ax = visuals.getEnrollmentVisual(df, coursecode)
	plt.ylabel("Number of Students")
	plt.tight_layout()
	plt.savefig(f"{EXPORT_DIR}/{quarter_name}_{coursecode}_enrollment_visual.svg", format = "svg")
	plt.close()


# Export data for all quarters listed in the shell call ( ./main w18 s18 ... )
if __name__ == "__main__":

	for quarter in sys.argv[1:]:
		df = getQuarterDF(quarter)

		print("Generating enrollment descriptions for " + quarter)
		df.CourseCode.unique().apply(lambda c: exportEnrollmentDescription(df, quarter, c))
	
	print("All done.")
