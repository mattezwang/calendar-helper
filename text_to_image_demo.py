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
date_format = '%m-%d-%Y'
dt_start = datetime.strptime('09-06-2022', date_format).date()
dt_end = datetime.strptime('12-20-2022', date_format).date()

weekdayofstart = dt_start.weekday()

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

def getStartingDate(day):

    offset = weekdayToLetter[day] - weekdayofstart
    return dt_start + timedelta(days=offset) if offset > 0 else dt_start + timedelta(days=(7+offset))

print(dt_start)
print(dt_end)


def parseText(text):
    df = pd.DataFrame(columns=["Subject", "Start Date", "Start Time", "End Date", 
                                "End Time", "All Day Event", "Description", "Location", "Private"])
    
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

        times = lines[3 + offset].split(' to ')
        start_time = times[0]
        end_time = times[1]

        date = getStartingDate(day)
        df.loc[len(df.index)] = [course, date, start_time, date, end_time, 'FALSE', '{} for {}'.format(lines[1+offset][:3], course), lines[2+offset], 'FALSE']
        offset = 0

    return df

def repeat_events(df):
    repeated_df = pd.DataFrame(columns=df.columns)

    for index, row in df.iterrows():
        start_date = row['Start Date']
        i = 0

        new_date = start_date + timedelta(weeks=i)

        while(dt_start <= new_date <= dt_end):

            repeated_df = pd.concat([
                repeated_df,
                pd.DataFrame({
                    'Subject': row['Subject'],
                    'Start Date': new_date,
                    'Start Time': row['Start Time'],
                    'End Date': new_date,
                    'End Time': row['End Time'],
                    'All Day Event': row['All Day Event'],
                    'Description': row['Description'],
                    'Location': row['Location'],
                    'Private': row['Private']
                }, index=[0])
            ])

            i+=1
            new_date = start_date + timedelta(weeks=i)

    return repeated_df

df = parseText(text)
df = repeat_events(df)
df.to_csv('calendar_example.csv', index=False)