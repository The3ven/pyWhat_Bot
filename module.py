"""
Schedule is an unofficial python whatsapp wrapper which is allowing you to send notification about class schedule. 
"""

import os
import time
from myenv import *
import traceback
from datetime import datetime
from alright import WhatsApp

class ClassShedular(object):
    def __init__(self) -> None:
        self.Sunday = self.get_time_in_sec("12:00:00")
        self.messenger = WhatsApp()
        self.messenger.fetch_all_unread_chats(limit=True, top=30)
        # self.messenger.browser.quit()
        
    
    def remtime(self, stime: int, ctime: int):
        remain = stime - ctime
        return remain

    def sleep_sunday(self):
        if self.get_day_name() == "Sunday":
            logger.warning("Today is Sunday, I need to rest for the day!")
            time.sleep(self.Sunday)

    def send_messegse(self, user, messages):
        self.messenger.find_user(user)
        for message in messages:
            self.messenger.send_message(message)

    def read_json(self,filename: str) -> dict:
        try:
            with open(filename, "r") as f:
                data = f.read()
        except IOError as bug:
            print("Could not read file:" + {bug})
        return dict(eval(data))

    def get_day_name(self):
        dt = datetime.now()
        wname = dt.strftime('%A')
        return wname

    def get_sys_time(self):
        CTime = datetime.today().strftime("%I:%M:%S %p")
        return CTime

    def get_sys_time_12_hr_sec(self):
        t = time.localtime(time.time())
        min_sec = t.tm_min*60
        hr_sec = t.tm_hour*60*60
        hour_12_sec = hr_sec % 12
        total_sec_12_hr = t.tm_sec + min_sec + hour_12_sec
        return total_sec_12_hr

    def get_json_data(self,formattedJson: str, day: str, filename: str, Time: str, course: str):
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


    def get_rtime(self,time: str):
        
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

        if hour == 0:
            remhr = "00"
        else:
            remhr = 12 - hour
            if len(str(remhr)) == 1:
                remhr = "0"+str(remhr)

        if min == 0:
            remmin = "00"
        else:
            remmin = 60 - min

        if sec == 0:
            remsec = "00"
        else:
            remsec = 60 - sec

        remaintime = str(remhr)+":"+str(remmin)+":"+str(remsec)
        return remaintime 

    def get_sys_time(self):
        CTime = datetime.today().strftime("%I:%M:%S %p")
        return CTime

    def get_class_time(self, filename: str, day: str):
        try:
            timetable_json = self.read_json(filename)
        except Exception as bug:
            print("Could not parse Json File" + {bug})
        try:
            Times = timetable_json["course"]["MCA"]["Days"][day]["Time"][0].keys()
        except Exception:
            print("Warning => We can`t Find Key For Discription Error : \n{}".format(
                traceback.format_exc()))

        return Times, timetable_json

    def get_time_in_sec(self,time: str):
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

    def start(self):
        self.sleep_sunday()
        last_flag = False
        while True:
            Times, timetable_json = self.get_class_time(MyJson, self.get_day_name())
            for Time in Times:
                print(Time)
                if Time == self.get_sys_time():
                    print(f"Last time we send notification {Time}")
                    print("Time For Class Sending Notification")
                    Sub, Sub_code, Prof, Description = self.get_json_data(
                        timetable_json, self.get_day_name(), MyJson, Time, Course1)

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
                    self.send_messegse(MNumber, message)
                    else_flag = True
                    last_flag == True
            # if last_flag == False:
            #     print("Running Bot First time")
            #     remsec = self.get_time_in_sec(self.get_rtime(self.get_sys_time()))
            #     sleepsec = self.get_time_in_sec(self.get_sys_time()) + remsec
            #     if self.get_time_in_sec(self.get_sys_time()) < sleepsec:
            #         print(
            #             f"Current time is {self.get_sys_time()} ...\nWe need to sleep till {sleepsec} second \ncurrent second is {self.get_time_in_sec(self.get_sys_time())} remain {sleepsec - self.get_time_in_sec(self.get_sys_time())}")
            #         time.sleep(sleepsec - self.get_time_in_sec(self.get_sys_time()) - 60)
            #     elif else_flag == True:
            #         sleep_sec = self.get_time_in_sec("01:00:00")
            #         print(f"Sleep for {sleep_sec} Second")
            #         time.sleep(sleep_sec)


if __name__ == "__main__":
    CSch = ClassShedular()
    CSch.start()
