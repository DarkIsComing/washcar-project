# for i in range(19)[9::-1]:
#     print(i)

import time
import datetime
from app.api_1_0.utils import timestamp_to_normal_time
# timestamp=1558762020195/1000
# time_array=time.localtime(timestamp)
# print(time_array)
# otherStyleTime = time.strftime("%Y--%m--%d %H:%M:%S", time_array)
# print(otherStyleTime)
# print(timestamp_to_normal_time('1558762020'))
# # print(len(1558762020195))
# # print(len('1558762020195'))

# timeStamp = 1558762020
# dateArray = datetime.datetime.fromtimestamp(timeStamp)
# otherStyleTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")
# print(otherStyleTime)   # 2013--10--10 15:40:00

# t=round(time.time())
# t13=round(time.time()*1000)
# print(int(t))
# print(t13)
# name=None
# lufei='lufei'
# d={}
# d.update({'piece':lufei})
# d.update({'name':name}) if name is not None
# print(d)

# t=(1,2,3)
# print(t,type(t))
# print(t[0])
import datetime
text='2016-7-10'
dd=datetime.datetime.strptime(text, '%Y-%m-%d')
print(dd.day)