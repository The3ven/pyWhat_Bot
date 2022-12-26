from datetime import datetime
from alright import WhatsApp
from dotenv import load_dotenv
import os



#Setup env
load_dotenv()
MNumber = os.environ.get("User_MN")

# Send Massege Function.
def send_messegse(user, messages):
    messenger = WhatsApp()
    messenger.find_user(user)
    for message in messages:
        messenger.send_message(message)


def get_Dayname():
    dt = datetime.now()
    wname = dt.strftime('%A')
    return wname


def get_Time():
    CTime = datetime.today().strftime("%I:%M %p")
    return CTime







if __name__ == "__main__":
    def main():
        message = ["hello boys how are you",
                   "Hope you will be well", get_Dayname(), get_Time()]
        print(type(message))
        # print(type(get_Dayname()))
        # messages = message + str(get_Dayname())
        send_messegse(MNumber, message)

main()
