from datetime import datetime
import traceback
from alright import WhatsApp
from dotenv import load_dotenv
import os


# Setup env
load_dotenv()
MNumber = os.environ.get("User_MN")
MyJson = os.environ.get("TimeTable")
Course1 = os.environ.get("Course1")


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


def read_json(filename: str) -> dict:
    try:
        with open(filename, "r") as f:
            data = f.read()
    except IOError as bug:
        print("Could not read file:" + {bug})
    return dict(eval(data))


def get_class_time(filename: str, day: str):
    try:
        timetable_json = read_json(filename)
    except Exception as bug:
        print("Could not parse Json File" + {bug})
    Times = timetable_json["course"]["MCA"]["Days"][day]["Time"][0].keys()
    return Times, timetable_json


def get_json_data(formattedJson: str, day: str, filename: str, Time: str, course: str):
    try:
        Sub = formattedJson["course"][course]["Days"][day]["Time"][0][Time][0]["Sub"]
    except Exception:
        print("Warning => We can`t Find Key For Subject Error : \n{}".format(
            traceback.format_exc()))
        Sub = None
    finally:
        pass

    try:
        Sub_code = formattedJson["course"][course]["Days"][day]["Time"][0][Time][0]["Sub_code"]
    except Exception:
        print("Warning => We can`t Find Key For Subject Code Error : \n{}".format(
            traceback.format_exc()))
        Sub_code = None
    finally:
        pass

    try:
        Prof = formattedJson["course"][course]["Days"][day]["Time"][0][Time][0]["Prof"]
    except Exception:
        print("Warning => We can`t Find Key For Professor Name Error : \n{}".format(
            traceback.format_exc()))
        Prof = None
    finally:
        pass

    try:
        Description = formattedJson["course"][course]["Days"][day]["Time"][0][Time][0]["Description"]
    except Exception:
        print("Warning => We can`t Find Key For Discription Error : \n{}".format(
            traceback.format_exc()))
        Description = None
    finally:
        pass
    
    return Sub, Sub_code, Prof, Description


if __name__ == "__main__":
    Times, timetable_json = get_class_time(MyJson, get_day_name())
    for Time in Times:
        if Time == get_sys_time():
            print("Time For Class Sending Notification")
            Sub, Sub_code, Prof, Description = get_json_data(
                timetable_json, get_day_name(), MyJson, Time, Course1)
            message = ["You have Class Guys :-", "Subject : " + Sub,
                       "Subject Code : " + Sub_code, "Professor : " + Prof, Description]
            send_messegse(MNumber, message)
