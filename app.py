import pandas as pd
from datetime import datetime, timedelta

text = '''Monday
ENGL 140:  Comm B Topics in English Literature
DIS 305
7117 Helen C. White Hall
12:05 PM to 12:55 PM

Tuesday
COMP SCI 540:  Introduction to Artificial Intelligence
LEC 002
1310 Sterling Hall
11:00 AM to 12:15 PM

COMP SCI 577:  Introduction to Algorithms
LEC 002
S413 Chemistry Building
1:00 PM to 2:15 PM

ENGL 140:  Comm B Topics in English Literature
LEC 001
1520 Microbial Sciences
9:55 AM to 10:45 AM

Wednesday
COMP SCI 577:  Introduction to Algorithms
DIS 322
2239 Engineering Hall
11:00 AM to 11:50 AM

ENGL 140:  Comm B Topics in English Literature
DIS 305
7117 Helen C. White Hall
12:05 PM to 12:55 PM

Thursday
COMP SCI 540:  Introduction to Artificial Intelligence
LEC 002
1310 Sterling Hall
11:00 AM to 12:15 PM

COMP SCI 577:  Introduction to Algorithms
LEC 002
S413 Chemistry Building
1:00 PM to 2:15 PM

ENGL 140:  Comm B Topics in English Literature
LEC 001
1520 Microbial Sciences
9:55 AM to 10:45 AM'''


# sample datetime, when i make it into a website have an input for it
date_format = '%Y%m%dT%I%M%S'

str_start = '20220906T120000'
str_end = '20221220T120000'
dt_start = datetime.strptime(str_start, date_format).date()
dt_end = datetime.strptime(str_end, date_format).date()

weekdayofstart = dt_start.weekday()

CalendarName = 'cal.ics'

weekdayToLetter = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6
}

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# DATETIME RETURN 
def getStartingDate(day):
    offset = weekdayToLetter[day] - weekdayofstart
    return (dt_start + timedelta(days=offset) if offset > 0 else dt_start + timedelta(days=(7+offset)))

# STRING RETURN
def convertDateFormat(time):
    return time.strftime('%Y%m%dT%I%M%S')[:-6]

def parseText(text):
    df = pd.DataFrame(columns=["Subject", "Start", "End", "Description", "Location"])
    
    blocks = text.split('\n\n')

    course = None
    offset = 0

    for block in blocks:
        lines = block.split('\n')

        if('day' in lines[0]):
            if any(lines[0] == d for d in days):
                day = lines[0]
                offset = 1

        course = lines[0 + offset][:lines[0 + offset].index(":"):]

        # this seperates times into ['X:XX AM', 'XX:XX PM'] 
        times = lines[3 + offset].split(' to ')

        # this seperates it into ['X', 'XX AM']
        start_time = times[0].split(":")
        end_time = times[1].split(":")

        # makes it so its converted into millitary time
        if(times[0][-2:] == 'PM' and start_time[0] != '12'):
            start_time[0] = int(start_time[0]) + 12
            end_time[0] = int(end_time[0]) + 12
        elif(times[1][-2:] == 'PM' and end_time[0] != '12'):
            end_time[0] = int(end_time[0]) + 12
        
        # this is a datetime object
        date = getStartingDate(day)
        st = "{}{}00".format(start_time[0], start_time[1][:2]).rjust(6, "0")
        et = "{}{}00".format(end_time[0], end_time[1][:2]).rjust(6, "0")


        df.loc[len(df.index)] = [course, convertDateFormat(date)+st, convertDateFormat(date)+et, '{} for {}'.format(lines[1+offset][:3], course), lines[2+offset]]
        offset = 0
    return df

df = parseText(text)

F = open(CalendarName, "w")
F.write("BEGIN:VCALENDAR\nPRODID:-ICSUW//MW//EN\nMETHOD:PUBLISH\nX-MS-OLK-FORCEINSPECTOROPEN:TRUE\nX-WR-CALNAME;VALUE=TEXT:" + CalendarName + "\n")
for index, row in df.iterrows():
    F.write("BEGIN:VEVENT\nCLASS:PUBLIC\n")
    F.write("DESCRIPTION:" + str(row['Description']) + "\n")
    F.write("LOCATION:" + row['Location'] + "\n")
    # F.write("DTSTAMP:" + row['Start Date'] + "T" + str(row['Start Time'])  + "\n")
    F.write("DTSTART:" + row['Start'] + "\n")
    F.write("DTEND:" + row['End'] + "\n")
    F.write("RRULE:FREQ=WEEKLY;UNTIL=" + str_end + "\n")
    F.write("UID:" + str(row['Subject']) + str(row['Start']) + str(row['End']) + "\n")
    F.write("PRIORITY:5" + "\n")
    F.write("SEQUENCE:0" + "\n")
    F.write("SUMMARY;LANGUAGE=en-us:" + str(row['Subject']) + "\n")
    F.write("X-MICROSOFT-CDO-ALLDAYEVENT:FALSE\nX-MICROSOFT-MSNCALENDAR-ALLDAYEVENT:FALSE\n")
    F.write("END:VEVENT" + "\n")

F.write("END:VCALENDAR")
