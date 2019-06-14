from app.api_1_0.utils import timestamp_to_normal_time,connect_to_mysql,get_state,connect_redis_produce,get_today_point_0,get_yesterday_point_0,cal_difftime, is_date
from config import LIST_NAME,REDIS_DB_URL_PRODUCE
import json
import time
from datetime import datetime
#处理昨日的数据
def update_yesterday_data():
    point_0_stamp=get_today_point_0()         #获取当日0点0分的10位时间戳。
    yesterday_point_0_stamp=get_yesterday_point_0()     #获取昨日0点0分的10位时间戳。
    conn=connect_redis_produce()
    con=connect_to_mysql()
    cursor=con.cursor()
    yesterday_data=[]
    flag=0
    wax=False
    bubble=False
    d={}
    for i in range(conn.llen(LIST_NAME)):
        single_data=str(conn.lindex(LIST_NAME,i),'utf-8')    #获取最新一条的洗车数据并转化成str
        single_data=json.loads(single_data)       #反序列化,转成dict类型  
        time_stamp=float(single_data['time'])/1000
        if time_stamp>=float(point_0_stamp):
            continue
        elif float(yesterday_point_0_stamp)<=time_stamp<float(point_0_stamp):
            single_data['state']=get_state(single_data)
            yesterday_data.append(single_data)
        else:
            break
    
    for data in yesterday_data[::-1]:
        if data['state']=='start':
            in_time=timestamp_to_normal_time(data['time'])      #str
            flag=1
            d['in_time']=in_time
            d['today'] = in_time.split()[0]
            #print(d['today'],type(d['today']))
        elif data['state']=='start_wax' and flag==1:
            wax=True
        elif data['state']=='start_bubble' and flag==1:
            bubble=True
            
        elif data['state']=='complete' and flag==1:
            out_time=timestamp_to_normal_time(data['time'])
            flag=0
            if wax==True and bubble==True:
                d['type']='wax_bubble_wash'        #泡沫水蜡洗
            elif wax==False and bubble==True:
                d['type']='bubble_wash'            #泡沫洗车
            elif wax==True and bubble==False:
                d['type']='wax_wash'            #抛光水蜡洗车
            else :
                d['type']='normal_wash'     #普通洗车
            d['out_time']=out_time
            d['time_delta']=cal_difftime(d['in_time'],d['out_time'])
            try:
                cursor.execute("INSERT INTO all_record (wash_type,in_time,out_time,date,time_delta) VALUES ('%s','%s','%s','%s','%s')"%(d['type'],d['in_time'],d['out_time'],d['today'],d['time_delta']))
                #cursor.execute("INSERT INTO all_record (wash_type,in_time,out_time,date,time_delta) VALUES ('%s','%s','%s','%s','%s')"%(**d))
                con.commit()
            except:
                con.rollback()
            wax=False
            bubble=False
            d.clear()  
        else:
            continue 
    cursor.close()
    con.close()  

update_yesterday_data()
    
# def get_today_point_0():
#     point_0_stamp=time.mktime(datetime.now().date().timetuple())
#     point_0=timestamp_to_normal_time(int(point_0_stamp))        #今日0点
#     return point_0

# def get_yesterday_point_0():
#     yesterday_point_0_stamp=time.mktime(datetime.now().date().timetuple())-86400
#     yesterday_point_0=timestamp_to_normal_time(int(yesterday_point_0_stamp))        #昨日0点
#     return yesterday_point_0

# t=get_today_point_0()
# y=get_yesterday_point_0()









#def get_today_zero_oclick():
#     cur_timestamp=int(time.time())
#     cur_timestamp=int(cur_timestamp-time.timezone)%86400
#     today_point_0=int(time.time())-cur_timestamp
#     today_point_24=point_0+86400
#     print(cur_timestamp)
#     print(timestamp_to_normal_time(int(time.time())))
#     print(time.timezone)
#     print(timestamp_to_normal_time(point_0)) #2019-05-28 00:00:00
#     print(timestamp_to_normal_time(point_24))   #2019-05-29 00:00:00