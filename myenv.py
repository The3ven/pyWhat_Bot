"""
env file to load all necessary environment variable for Class_Shedule Script 
"""



from dotenv import load_dotenv
import logging
import os


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
