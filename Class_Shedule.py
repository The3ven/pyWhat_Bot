from datetime import datetime
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
    CTime = datetime.today().strftime("%I:%M %p")
    return CTime


def read_json(filename: str) -> dict:
    with open(filename, "r") as f:
        data = f.read()

    return dict(eval(data))


def get_class_time(filename: str, day: str):
    timetable_json = read_json(filename)
    Times = timetable_json["course"]["MCA"]["Days"][day]["Time"][0].keys()
    return Times, timetable_json


def get_json_data(formattedJson: str, day: str, filename: str, Time: str, course: str):
    Sub = formattedJson["course"][course]["Days"][day]["Time"][0][Time][0]["Sub"]
    Sub_code = formattedJson["course"][course]["Days"][day]["Time"][0][Time][0]["Sub_code"]
    Prof = formattedJson["course"][course]["Days"][day]["Time"][0][Time][0]["Prof"]
    Description = formattedJson["course"][course]["Days"][day]["Time"][0][Time][0]["Description"]
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
