import redis
from config import REDIS_DB_URL_PRODUCE,LIST_NAME
import time
import json
import pymysql
from datetime import datetime
#连接redis
# def connect_redis_local():
#     return redis.StrictRedis(**REDIS_DB_URL_LOCAL)

def connect_redis_produce():
    return redis.StrictRedis(**REDIS_DB_URL_PRODUCE)

#get key
def get_redis_data(key):
    conn = connect_redis_produce()
    data = conn.get(key)
    return data

#set key
def set_redis_data(key, value):
    conn = connect_redis_produce()
    data = value
    conn.set(
        name=key,
        value=data
        # ex=config.EXPIRES_TIME  # 第三个参数表示Redis过期时间,不设置则默认不过期
    )

# def set_redis_list(key,value):
#     conn = connect_redis()
#     data = value
#     conn.rpush(name=key,*values)
    

def show_redis_list(key,start,stop):
    conn = connect_redis_produce()
    result=conn.lrange(name=key,start=start,end=stop)
    return result

#13位或10位时间戳转正常时间。
def timestamp_to_normal_time(timestamp):
    timestamp=str(timestamp)
    if len(timestamp)==13:
        timestamp_10=int(timestamp)/1000 
        
    elif len(timestamp)==10:
        timestamp_10=int(timestamp)
    else:
        return None
    time_array=time.localtime(timestamp_10)
    normal_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    return normal_time

#获取实时状态
def get_state(real_time_data):
    if isinstance(real_time_data,dict) and 'car_mode' in real_time_data.keys() and 'value' in real_time_data.keys():
        if real_time_data['car_mode']=='car_forward' and real_time_data['value']=='1':
            return None
        if real_time_data['car_mode']=='car_forward' and real_time_data['value']=='0':
            return None
        if real_time_data['car_mode']=='car_back' and real_time_data['value']=='1':
            return None
        if real_time_data['car_mode']=='car_back' and real_time_data['value']=='0':
            return None
        if real_time_data['car_mode']=='car_washcomplete' and real_time_data['value']=='0':
            return 'start'
        if real_time_data['car_mode']=='car_washcomplete' and real_time_data['value']=='1':
            return 'complete'
        if real_time_data['car_mode']=='car_washfailure' and real_time_data['value']=='1':
            return 'failure'
        
        if real_time_data['car_mode']=='car_in_pos' and real_time_data['value']=='1':
            return 'get_in_position'
        if real_time_data['car_mode']=='car_in_pos' and real_time_data['value']=='0':
            return 'position_ok'
        
        if real_time_data['car_mode']=='car_wash' and real_time_data['value']=='1':
            return 'start_wash'
        if real_time_data['car_mode']=='car_wash'and real_time_data['value']=='0':
            return 'finish_wash'
        if real_time_data['car_mode']=='car_bubble'and real_time_data['value']=='1':
            return 'start_bubble'
        if real_time_data['car_mode']=='car_bubble'and real_time_data['value']=='0':
            return 'finish_bubble'
        if real_time_data['car_mode']=='car_blow'and real_time_data['value']=='1':
            return 'start_blow'
        if real_time_data['car_mode']=='car_blow'and real_time_data['value']=='0':
            return 'finish_blow'
        if real_time_data['car_mode']=='car_wax'and real_time_data['value']=='1':
            return 'start_wax'
        if real_time_data['car_mode']=='car_wax'and real_time_data['value']=='0':
            return 'finish_wax'
        if real_time_data['car_mode']=='car_clean'and real_time_data['value']=='1':
            return 'push_water'
        if real_time_data['car_mode']=='car_clean'and real_time_data['value']=='0':
            return 'end_push'
    else:
        return None





    
def set_hash(name,key,value):
    conn=connect_redis_produce()
    conn.hset(name,key,value)

def get_hash_if_exists(name,key):
    conn=connect_redis_produce()
    if conn.hexists(name,key):
        value=conn.hget(name,key)
        return value
    else:
        return None



def connect_to_mysql():
    con=pymysql.connect(host='localhost',port=3306,user='root',password='woaini123..',database="washcar",charset='utf8')
    return con

def get_today_point_0():
    point_0_stamp=time.mktime(datetime.now().date().timetuple())      #当日零点的10位时间戳
    point_0=timestamp_to_normal_time(int(point_0_stamp))        #今日0点
    return point_0_stamp

def get_yesterday_point_0():
    yesterday_point_0_stamp=time.mktime(datetime.now().date().timetuple())-86400
    yesterday_point_0=timestamp_to_normal_time(int(yesterday_point_0_stamp))        #昨日0点
    return yesterday_point_0_stamp


#计算时间差
def cal_difftime(date1, date2):
    if is_date(date1) and is_date(date2): 
        date3=datetime.strptime(date1,"%Y-%m-%d %H:%M:%S")  # 字符串转换为datetime类型
        date4=datetime.strptime(date2,"%Y-%m-%d %H:%M:%S")  # 字符串转换为datetime类型
        times = str(date4 - date3).split(':')
        difftime = times[0]+'时'+times[1]+'分'+times[2]+'秒'    
        return difftime

#判断日期是否为合法输入，年月日的格式需要与上面对应，正确返回True，错误返回False，注意大小写。
def is_date(date):
    try:
        datetime.strptime(date,"%Y-%m-%d %H:%M:%S")
        return True
    except:
        return False


def test1():
    print('bob')

def test2():
    print('aoa')
    


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