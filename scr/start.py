import schedule
import time
from txt_reader import *
from screenshot import *
import time
from date import *
tgid, timetabel, id, date_of_week, time1 = read()
date_of_week = 'thu'
time1 = '18:14'
if date_of_week =='mon':
    schedule.every().monday.at(time1).do(main1)
elif date_of_week =='tue':
    schedule.every().tuesday.at(time1).do(main1)
elif date_of_week == 'wed':
    schedule.every().wednesday.at(time1).do(main1)
elif date_of_week == 'thu':
    schedule.every().thursday.at(time1).do(main1)
elif date_of_week == 'fri':
    schedule.every().friday.at(time1).do(main1)
elif date_of_week == 'sat':
    schedule.every().saturday.at(time1).do(main1)
elif date_of_week == 'sun':
    schedule.every().sunday.at(time1).do(main1)


while True:
    schedule.run_pending()
    print(schedule.get_jobs())
    time.sleep(10)



