from datetime import datetime
from alright import WhatsApp
from dotenv import load_dotenv
import os


# Setup env
load_dotenv()
MNumber = os.environ.get("User_MN")
MyJson = os.environ.get("TimeTable")
Course1 = os.environ.get("Course1")

# Send Massege Function.


def send_messegse(user, messages):
    messenger = WhatsApp()
    messenger.find_user(user)
    for message in messages:
        messenger.send_message(message)


def get_Dayname():
    dt = datetime.now()
    wname = dt.strftime('%A')
    return "Monday"


def get_SysTime():
    CTime = datetime.today().strftime("%I:%M %p")
    return CTime


def read_json(filename: str) -> dict:
    with open(filename, "r") as f:
        data = f.read()

    return dict(eval(data))


def get_ClassTime(filename: str, day: str):
    timetable_json = read_json(filename)
    Times = timetable_json["course"]["MCA"]["Days"][day]["Time"][0].keys()
    return Times, timetable_json


def getJsonData(formattedJson: str, day: str, filename: str, Time: str, course: str):
    Sub = formattedJson["course"][course]["Days"][day]["Time"][0][Time][0]["Sub"]
    Sub_code = formattedJson["course"][course]["Days"][day]["Time"][0][Time][0]["Sub_code"]
    Prof = formattedJson["course"][course]["Days"][day]["Time"][0][Time][0]["Prof"]
    Description = formattedJson["course"][course]["Days"][day]["Time"][0][Time][0]["Description"]
    return Sub, Sub_code, Prof, Description


if __name__ == "__main__":
    Times, timetable_json = get_ClassTime(MyJson, get_Dayname())
    for Time in Times:
        if Time == get_SysTime():
            print("Time For Class Sending Notification")
            Sub, Sub_code, Prof, Description = getJsonData(
                timetable_json, get_Dayname(), MyJson, Time, Course1)
            message = ["You have Class Guys :", "Subject : " + Sub,
                       "Subject Code :" + Sub_code, "Professor " + Prof, Description]
            send_messegse(MNumber, message)
