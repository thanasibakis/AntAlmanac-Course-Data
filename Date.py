# Description: a class representation of an enrollment date
# Author: Thanasi Bakis

# A date code is the integer index of the possible enrollment dates
# Converts a date code (0, 1, 2) to something human-readable (mon wk 8, tues wk 8, ...)
DATECODE_TO_TEXT = ("Monday of week 8", "Tuesday of week 8", "Wednesday of week 8", "Thursday of week 8", "Friday of week 8", "Saturday of week 8", "Sunday of week 8",
                    "Monday of week 9", "Tuesday of week 9", "Wednesday of week 9", "Thursday of week 9", "Friday of week 9", "Saturday of week 9", "Sunday of week 9",
                    "Monday of week 10", "Tuesday of week 10", "Wednesday of week 10", "Thursday of week 10", "Friday of week 10", "Saturday of week 10", "Sunday of week 10",
                    "Monday of finals week", "Tuesday of finals week", "Wednesday of finals week", "Thursday of finals week", "Friday of finals week",
                    "Monday of week 1", "Tuesday of week 1", "Wednesday of week 1", "Thursday of week 1", "Friday of week 1", "Saturday of week 1", "Sunday of week 1",
                    "Monday of week 2", "Tuesday of week 2", "Wednesday of week 2", "Thursday of week 2", "Friday of week 2")

class Date:
    
    MAX_DATECODE = len(DATECODE_TO_TEXT) - 1

    def __init__(self, dateCode):
        self.dateCode = dateCode
     
    def __repr__(self): # the full text version
        return DATECODE_TO_TEXT[self.dateCode]

    def __float__(self): # matplotlib wants this for plotting on an axis
        return float(self.dateCode)

    def abbreviate(self): # the abbreviated version
        text = str(self)

        if "finals" in text:
            return text[0] + "f"

        return text[0] + text.split(" ")[-1]

    def __eq__(self, other):
        if type(other) == Date:
            return self.dateCode == other.dateCode

        return self.dateCode == other  # in the event we pass in a date code integer
    
    def __lt__(self, other):
        if type(other) == Date:
            return self.dateCode < other.dateCode

        return self.dateCode < other
    
    def __hash__(self): # pandas wants this to store Dates in a table
        return hash(self.dateCode)
