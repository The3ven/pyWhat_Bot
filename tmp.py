from datetime import datetime
import json
import time
import sys


def get_SysTime():
    CTime = datetime.today().strftime("%I:%M %p")
    return CTime


def read_json(filename: str) -> dict:
    try:
        with open(filename, "r") as f:
            data = f.read()
    except FileExistsError as bug:
        print("Log: Error - {bug}")
    else:
        return dict(eval(data))




        



# def getJsonData(day: str, filename: str, Time: str, course: str):
    
    
#     Sub = timetable_json["course"][course]["Days"][day]["Time"][0][Time][0]["Sub"]
#     Sub_code = timetable_json["course"][course]["Days"][day]["Time"][0][Time][0]["Sub_code"]
#     Prof = timetable_json["course"][course]["Days"][day]["Time"][0][Time][0]["Prof"]
#     Description = timetable_json["course"][course]["Days"][day]["Time"][0][Time][0]["Description"]
#     # return Times, Sub, Sub_code, Prof, Description
#     return Times


# def match_Time():
    
#     Times = getJson("Monday", "timetable.json", "10 AM", "MCA")
#     # , Sub, Sub_code, Prof, Description

#     print(Times)
    # print(str(Sub))
    # print(Sub_code)
    # print(Prof)
    # print(Description)
    # for time in times:
    #     if time == get_Time():
    #         print("Time For Class Sending Notification")
    #     else:
    #         print("We need to wait for Next time")
    # print("Time is :" + str(times))
    # print("Subject is : " + Sub)


# while True:
#     try :
#         match_Time()
#     except OSError as bug:
#         print("Log : {bug}")
#     # sys.exit("Bye Bye")


# with open("timetable.json", "r") as f:
#     data = json.load(f)

# day = "Monday"
# Time = "9 AM"


# print(times)
# # for value in values:
# #     print(value)


get_ClassTime("timetable.json", "Monday")




    for Time in Times:
        if Time == get_SysTime():
            print("Time For Class Sending Notification")
            return timetable_json, Time, day