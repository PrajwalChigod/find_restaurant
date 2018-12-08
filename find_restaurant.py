'''

Name : find_restaurant.csv
Description : Find restaurant that are open
Input : CSV file & time 
output : list of restaurant that are open duirng the time 
usage : python - <filename.py> <datetime>
example - execute the script - enter input as prompted
    restaurant.csv
    01-12-2018 9:45 am


author : Prajwal Chigod

'''

import time
import datetime
import csv
import re
import calendar
import pandas as pd


weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
remaining_restaurants = []
datafile = input("Enter the name of the file : ").strip()
userinput = input("Enter the date in dd-mm-yyyy format and time in hh:mm[am/pm] format : ").strip().split(' ', 1)
try:
    restaurant_dict = {row[0]: row[1].split('/') for _, row in pd.read_csv(datafile, header=None).iterrows()}
except FileNotFoundError:
    print("CSV file not found!! - Please check!!")
try:
    userdate = userinput[0].strip()
    user_day = time.strftime("%a", time.strptime(userdate, "%d-%m-%Y"))
    user_time = userinput[1].strip()
except:
    print("please enter as guided!!")


def find_restaurant(datafile, userinput):
    # main function - takes 2 parameters - datafile [csv containing restaurant data] and userinput [ datetime object given by user ]
    for key, values in restaurant_dict.items():
        for i in values:
            if (get_time_info(i) and get_week_info(i)) == True:
                remaining_restaurants.append(key)
    
    print(remaining_restaurants)


def check_week_days(input_day, days, *optional_day):
    #checks whether the given weekday is present within the set of weekdays present in data file - takes 2 parmeters and 1 optional parameters
    if len(input_day) > 6:
        startday, endday = input_day.split('-')
        remaining_days = weekdays[weekdays.index(startday):weekdays.index(endday)]
    else:
        remaining_days = [input_day.replace(' ', '')]
    if days in remaining_days:
        return True
    else:
        return False


def get_week_info(weekdays):
    #extracts info about days from csv file which can be used as input for check_week_days function - takes 1 parameters
    present_days = re.findall(r'[A-Z][a-z]*\s*-*[A-Z]*[a-z]*', weekdays)
    firstset = present_days[0]
    if len(present_days) > 1:
        optionalset = present_days[1]
        return(check_week_days(firstset, user_day, optionalset))
    else:
        return(check_week_days(firstset, user_day))


def check_time(start_time, end_time, requiredtime=user_time):
    #checks whether the given time is present within the set of time given in the data file - takes 2 parameters and 1default parameters
        starttime = convert_time(start_time)
        endtime = convert_time(end_time)
        requiredtime = convert_time(requiredtime)
        if starttime < requiredtime < endtime:
            return True
        else:
            return False


def convert_time(input_time):
    # converts the time to proper format which can be used in get_time_info function
    if ':' in input_time:
        strt = time.strptime(input_time, '%I:%M %p')
        return(time.strftime('%H:%M', strt))
    else:
        strt = time.strptime(input_time, '%I %p')
        return(time.strftime('%H', strt))


def get_time_info(weekdays):
    #extracts info about time from csv file which can be used as input for check_time function
    timings = re.findall(r'[0-9][0-9]*:*[0-9]* [a-z]m', weekdays)
    start_time = timings[0]
    end_time = timings[1]
    return(check_time(start_time, end_time))

find_restaurant(datafile, userinput)