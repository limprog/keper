import schedule
import time
from txt_reader import *
from screenshot import *
import time
from date import *
tgid, timetabel, id, date_of_week, time1 = read()
date_of_week = 'y'
time1 = '10:12'
scr = Screenshoot(today)
if date_of_week =='Mon':
    schedule.every().monday.at(time1).do(main())
elif date_of_week =='Tue':
    schedule.every().tuesday.at(time1).do(main())
elif date_of_week == 'Wed':
    schedule.every().wednesday.at(time1).do(main())
elif date_of_week == 'Thu':
    schedule.every().tuesday.at(time1).do(main())
elif date_of_week == 'Fri':
    schedule.every().friday.at(time1).do(main())
elif date_of_week == 'Sat':
    schedule.every().saturday.at(time1).do(main())
elif date_of_week == 'Sun':
    schedule.every().sunday.at(time1).do(main())
elif date_of_week == "y":
    schedule.every().tuesday.at(time1).do(main())



while True:
    schedule.run_pending()
    time.sleep(10)



