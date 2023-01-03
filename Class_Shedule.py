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
file_handler = logging.FileHandler('Shedule.log')
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


def get_time_in_sec(time: str = get_sys_time()):
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


def get_sys_time_24_hr_sec():
    t = time.localtime(time.time())
    min_sec = t.tm_min*60
    hr_24_sec = t.tm_hour*60*60
    total_sec_24_hr = t.tm_sec + min_sec + hr_24_sec
    return total_sec_24_hr


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
    Times, timetable_json = get_class_time(MyJson, get_day_name())
    total_sec_24_hr = get_sys_time_24_hr_sec()
    last_flag = False
    Sleep_from_evening = (60*60*16 - 5)
    count = 0
    sleep_flag = 0
    while True:
        if get_sys_time_12_hr_sec() == 18000:
            time.sleep(Sleep_from_evening)
        if get_sys_time_24_hr_sec() < 32395:
            while get_sys_time_24_hr_sec() < 32395:
                logger.info("Sleeping For {} \nsleep from {} Minutes".format(
                    remtime(32390, get_sys_time_24_hr_sec()), sleep_flag*10))
                time.sleep(get_time_in_sec("00:10:00"))
                sleep_flag + 1
        for Time in Times:
            if Time == get_sys_time():
                global last_time_run
                last_time_run = Time
                last_flag = True
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
            else:
                count = count + 1
                if (count == 6):
                    count = 0
                    if last_flag == False:
                        logger.warning("Running Bot First time")
                        while get_sys_time_24_hr_sec() > 61139:
                            logger.warning("Current time is \n{} ...\nWe need to sleep till Morning\nsleep from {} Minutes...".format(
                                get_sys_time(), sleep_flag*10))
                            print("Taking 5 minute power nap")
                            time.sleep(get_time_in_sec("00:10:00"))
                            sleep_flag + 1
                    else:
                        sleep_sec = get_time_in_sec("00:59:30")
                        logger.info("Sleep for {} Second".format(sleep_sec))
                        time.sleep(sleep_sec)


if __name__ == "__main__":
    start = get_time_in_sec("00:00:03")
    start_time = get_sys_time_12_hr_sec() + start
    while True:
        remain = remtime(start_time, get_sys_time_12_hr_sec())
        print(
            "Our Notification Bot Will Start in {}".format(remain))
        if get_sys_time_12_hr_sec() == start_time:
            main()
        else:
            time.sleep(1)
