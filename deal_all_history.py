from app.api_1_0.utils import timestamp_to_normal_time, connect_to_mysql, get_state, connect_redis_produce, \
    get_today_point_0, cal_difftime, is_date
from config import LIST_NAME,REDIS_DB_URL_PRODUCE
import json
import pymysql


def deal_all_record():
    conn=connect_redis_produce()
    con=connect_to_mysql()
    cursor=con.cursor()
    flag=0
    wax=False
    bubble=False
    d={}
    for i in range(conn.llen(LIST_NAME))[::-1]:
        data=str(conn.lindex(LIST_NAME,i),'utf-8')
        data=json.loads(data)       #反序列化,dict类型
        data['state']=get_state(data)
        if data['state']=='start':
            today_zero_point=get_today_point_0()
            #print(today_zero_point,data['time'])
            if float(data['time']//1000)-float(today_zero_point)>=0:
                break
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

deal_all_record()