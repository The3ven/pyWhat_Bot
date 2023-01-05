#!/bin/python3

import logging
from datetime import datetime
import traceback
from alright import WhatsApp
from dotenv import load_dotenv
import os
import time

# Setup env
load_dotenv()
MNumber = os.environ.get("User_MN")
MyJson = os.environ.get("TimeTable")
Course1 = os.environ.get("Course1")

# Set log file in Document dir
home_directory = os.path.expanduser('~')
logpath = os.path.join(home_directory, 'Documents', 'Shedule.log')


# Add log handlers
logger = logging.getLogger()
logger.setLevel(logging.NOTSET)

# our first handler is a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)
console_handler_format = '%(asctime)s | %(levelname)s: %(message)s'
console_handler.setFormatter(logging.Formatter(console_handler_format))
logger.addHandler(console_handler)

# the second handler is a file handler
file_handler = logging.FileHandler(logpath)
file_handler.setLevel(logging.INFO)
file_handler_format = '%(asctime)s | %(levelname)s | %(lineno)d: %(message)s'
file_handler.setFormatter(logging.Formatter(file_handler_format))
logger.addHandler(file_handler)


def remtime(stime: int, ctime: int):
    remain = stime - ctime
    return (remain)


def sleep_sunday():
    Sunday = get_time_in_sec("12:00:00")
    if get_day_name() == "Sunday":
        logger.warning("Today is Sunday, I need to rest for the day!")
        time.sleep(Sunday)


def send_messegse(user, messages):
    messenger = WhatsApp()
    messenger.find_user(user)
    for message in messages:
        messenger.send_message(message)


def get_day_name():
    dt = datetime.now()
    wname = dt.strftime('%A')
    return wname


def get_sys_time():
    CTime = datetime.today().strftime("%I:%M:%S %p")
    return CTime


def get_sys_time_12_hr_sec():
    t = time.localtime(time.time())
    min_sec = t.tm_min*60
    hr_sec = t.tm_hour*60*60
    hour_12_sec = hr_sec % 12
    total_sec_12_hr = t.tm_sec + min_sec + hour_12_sec
    return total_sec_12_hr


def get_time_in_sec(time: str):
    if time.endswith("AM"):
        time = time.replace("AM", "")
    else:
        time = time.replace("PM", "")
    t = time.split(":")
    h = t[0]
    m = t[1]
    s = t[2]
    hour = int(h)
    min = int(m)
    sec = int(s)
    sec_hour = hour*60*60
    sec_min = min*60
    total_sec = sec_hour + sec_min + sec
    return total_sec


def get_rtime(time: str):
    if time.endswith("AM"):
        time = time.replace("AM", "")
    else:
        time = time.replace("PM", "")

    t = time.split(":")
    h = t[0]
    m = t[1]
    s = t[2]
    hour = int(h)
    min = int(m)
    sec = int(s)
    if hour in range(13):
        if min in range(60):
            remmin = 60 - min
            if sec in range(60):
                remsec = 60 - sec
    remaintime = "00:"+str(remmin)+":"+str(remsec)
    return remaintime

# def get_sys_time_24_hr_sec():
#     t = time.localtime(time.time())
#     min_sec = t.tm_min*60
#     hr_24_sec = t.tm_hour*60*60
#     total_sec_24_hr = t.tm_sec + min_sec + hr_24_sec
#     return total_sec_24_hr


def read_json(filename: str) -> dict:
    try:
        with open(filename, "r") as f:
            data = f.read()
    except IOError as bug:
        logger.warning("Could not read file:" + {bug})
    return dict(eval(data))


def get_class_time(filename: str, day: str):
    try:
        timetable_json = read_json(filename)
    except Exception as bug:
        logger.warning("Could not parse Json File" + {bug})
    try:
        Times = timetable_json["course"]["MCA"]["Days"][day]["Time"][0].keys()
    except Exception:
        logger.warning("Warning => We can`t Find Key For Discription Error : \n{}".format(
            traceback.format_exc()))

    return Times, timetable_json


def get_json_data(formattedJson: str, day: str, filename: str, Time: str, course: str):
    try:
        Sub = formattedJson["course"][course]["Days"][day]["Time"][0][Time][0]["Sub"]
    except Exception:
        logger.warning("Warning => We can`t Find Key For Subject Error : \n{}".format(
            traceback.format_exc()))
        Sub = None
    finally:
        pass

    try:
        Sub_code = formattedJson["course"][course]["Days"][day]["Time"][0][Time][0]["Sub_code"]
    except Exception:
        logger.warning("Warning => We can`t Find Key For Subject Code Error : \n{}".format(
            traceback.format_exc()))
        Sub_code = None
    finally:
        pass

    try:
        Prof = formattedJson["course"][course]["Days"][day]["Time"][0][Time][0]["Prof"]
    except Exception:
        logger.warning("Warning => We can`t Find Key For Professor Name Error : \n{}".format(
            traceback.format_exc()))
        Prof = None
    finally:
        pass

    try:
        Description = formattedJson["course"][course]["Days"][day]["Time"][0][Time][0]["Description"]
    except Exception:
        logger.warning("Warning => We can`t Find Key For Discription Error : \n{}".format(
            traceback.format_exc()))
        Description = None
    finally:
        pass

    return Sub, Sub_code, Prof, Description


def main():
    sleep_sunday()
    last_flag = False
    while True:
        print("Hello")
        Times, timetable_json = get_class_time(MyJson, get_day_name())
        for Time in Times:
            print(f"Time is {Time}")
            print(
                f"Current time is :- {get_sys_time()}")
            if Time == get_sys_time():
                logger.info(f"Last time we send notification {Time}")
                logger.warning("Time For Class Sending Notification")
                Sub, Sub_code, Prof, Description = get_json_data(
                    timetable_json, get_day_name(), MyJson, Time, Course1)

                if Sub is not None:
                    message = ["You have Class Guys :-"]
                    message = message + ["Subject : " + Sub]
                else:
                    message = []
                if Sub_code is not None:
                    message = message + ["Subject Code : " + Sub_code]
                if Prof is not None:
                    message = message + ["Professor : " + Prof]
                if Description is not None:
                    message = message + [Description]
                send_messegse(MNumber, message)
                else_flag = True
        if last_flag == False:
            print("Running Bot First time")
            remsec = get_time_in_sec(get_rtime(get_sys_time()))
            sleepsec = get_time_in_sec(get_sys_time()) + remsec
            print(f"Remain is {remsec} current is {get_time_in_sec(get_sys_time())} mix seconds is {sleepsec}")
            if get_time_in_sec(get_sys_time()) < sleepsec:
                print(
                    f"Current time is ::- {get_sys_time()} ...\nWe need to sleep till {sleepsec} second \ncurrent second is {get_time_in_sec(get_sys_time())} remain {sleepsec - get_time_in_sec(get_sys_time())}")
                time.sleep(sleepsec - get_time_in_sec(get_sys_time()) - 60 )
            elif else_flag == True:
                sleep_sec = get_time_in_sec("01:00:00")
                print(f"Sleep for {sleep_sec} Second")
                time.sleep(sleep_sec)


if __name__ == "__main__":
    start = get_time_in_sec("00:00:03")
    start_time = get_sys_time_12_hr_sec() + start
    dot = "."
    pdot = "."
    print(
        "Our Notification Bot Will Start in ...")
    while True:
        remain = remtime(start_time, get_sys_time_12_hr_sec())
        print(f"{remain}" + f"{dot}")
        dot = dot + pdot
        if get_sys_time_12_hr_sec() == start_time:
            main()
        else:
            time.sleep(1)
