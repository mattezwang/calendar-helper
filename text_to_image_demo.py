from PIL import Image 
from pytesseract import pytesseract 
import cv2
import pandas as pd
from datetime import datetime, timedelta


# could definitely optimize it further by making the day of week checker better with hashmap maybe? also can combine discussion and lecture
# checker, and just have a varaible thats lecture or discussion

# sample datetime, when i make it into a website have an input for it
date_format = '%m-%d-%Y'
dt_start = datetime.strptime('09-06-2022', date_format).date()
dt_end = datetime.strptime('12-20-2022', date_format).date()

weekdayofstart = dt_start.weekday()

weekdayToLetter = {
    "M": 0,
    "T": 1,
    "W": 2,
    "R": 3,
    "F": 4,
    "S": 5,
    "S": 6
}

# day is a MWF or something

def getStartingDate(day):

    offset = weekdayToLetter[day] - weekdayofstart
    return dt_start + timedelta(days=offset) if offset > 0 else dt_start + timedelta(days=(7+offset))

print(dt_start)
print(dt_end)

def putCourse(line, type, name, df):
    info = line.split(" ")

    classDays = info[1]
    times = (info[2]+info[3]+info[4]).split("-")
    startTime = times[0]
    endTime = times[1]

    for day in classDays:
        if(day == "_"):
            continue
        else:
            date = getStartingDate(day)
            df.loc[len(df.index)] = [name, date, startTime[:-2] + " " + startTime[-2:], date, endTime[:-2] + " " + endTime[-2:], "FALSE", "{} for {}".format(type, name), None, 'FALSE']

def parseAllInfo(text):
    df = pd.DataFrame(columns=["Subject", "Start Date", "Start Time", "End Date", 
                               "End Time", "All Day Event", "Description", "Location", "Private"])
    
    lines = text.splitlines()

    currCourse = None

    for line in lines:

        #we have found a new course
        if(line.find("credit") != -1):
            #if(line != lines[0]):
            currCourse = line[:-13] if line.find("credits") != -1 else line[:-12]

        elif(line.find("LEC") == 0):
            if(line.find("Online") != -1):
                continue
            else:
                putCourse(line, "Lecture", currCourse, df)

        #we have found the discussion line of info
        elif(line.find("DIS") == 0):
            putCourse(line, "Discussion", currCourse, df)

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


# Passing the image object to image_to_string() function 
# This function will extract the text from the image 
img = cv2.imread(r"images/try1.png", 0)
text = pytesseract.image_to_string(img) 
df = parseAllInfo(text)

df = repeat_events(df)

df.to_csv('calEx1.csv', index=False)