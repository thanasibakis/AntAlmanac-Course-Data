# Description: a library of functions to plot course enrollment data
# Author: Thanasi Bakis


import seaborn as sns
import pandas as pd
import language
from Date import Date
import matplotlib as mpl

sns.set_style("whitegrid")


# Generates a lineplot of the course's enrollment trends in the given quarter's data frame.
def getEnrollmentVisual(df, coursecode):

    # Our df was semi-longform (longform with respect to coursecode-date, but wideform wrt. date-count),
    # but we now want to expand each student count (enr, max, req, wl) for each date
    # (since there's only one course we're examining now)
    df = df[df.CourseCode == coursecode]
    df_long = pd.melt(df,
                      id_vars=["Date"],
                      value_vars=["Maximum", "Enrolled", "Requested", "Waitlist"],
                      var_name="Type",
                      value_name="Count")

    ax = sns.lineplot(x="Date", y="Count", hue="Type", data=df_long)

    # Convert the date code tick labels to date abbreviations
    ax.xaxis.set_major_formatter(
        mpl.ticker.FuncFormatter(_tickFloatToLabel)
    )
    return ax

# Since plots can't sort date text in chronological order,
# we let them use the date code numeric values and then manually
# override the tick labels to recreate the abbreviations
def _tickFloatToLabel(value, position):
    if (value > Date.MAX_DATECODE): # the plot may try to extend the axis past the last date we use
        return ''

    return Date(int(value)).abbreviate()