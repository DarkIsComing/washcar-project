import time  
from datetime import datetime
  
# date1='2019-05-27 19:19:53'
# date2='2019-05-28 08:14:52'
t=time.mktime(datetime.now().date().timetuple())
print(t)