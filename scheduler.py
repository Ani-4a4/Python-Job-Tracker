import schedule
import time
from main import job_check

print('Job tracker started and will run every 6 hours')
print('Press Ctrl + C to stop the tracker')

schedule.every(6).hours.do(job_check)

job_check()

try:
    while True:
        schedule.run_pending()
        time.sleep(60)
except KeyboardInterrupt:
    print('Tracker has been stopped')
    