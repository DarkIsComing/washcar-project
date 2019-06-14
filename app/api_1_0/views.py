from . import api
from .utils import  connect_redis_produce, get_redis_data, set_redis_data, show_redis_list, \
timestamp_to_normal_time, get_state,set_hash,get_hash_if_exists,get_today_point_0, get_yesterday_point_0,\
connect_to_mysql
import json
from flask import render_template,jsonify,request
from config import LIST_NAME
import time
from datetime import datetime
@api.route('/',methods=['GET','POST'])
def index():
    conn=connect_redis_produce()
    con=connect_to_mysql()
    real_time_data=str(conn.lindex(LIST_NAME,0),'utf-8')    #获取最新一条的洗车数据并转化成str
    real_time_data=json.loads(real_time_data)       #反序列化,转成dict类型 
    time=timestamp_to_normal_time(real_time_data['time'])   #把时间戳转成正常的显示时间
    state1=get_state(real_time_data)  
    items=[]           #获取当前洗车处在的状态。
    for i in range(conn.llen(LIST_NAME))[:150:]:
        data=str(conn.lindex(LIST_NAME,i),'utf-8')
        data=json.loads(data)       #反序列化,dict类型 
        single_state=get_state(data)
        #print(data['time'],type(data['time']))
        data['time']=timestamp_to_normal_time(data['time'])
        if single_state:
            data['single_state']=single_state        
            items.append(data)
    state=items[0]['single_state']
    cursor=con.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM all_record")
        count=cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM all_record where wash_type='bubble_wash'")
        bubble_count=cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM all_record where wash_type='wax_bubble_wash'")
        wax_bubble_count=cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM all_record where wash_type='normal_wash'")
        normal_count=cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM all_record where wash_type='wax_wash'")
        wax_count=cursor.fetchone()[0]
    except:
        con.rollback()
    return render_template('state.html',time=time,state=state,items=items,\
        count=count,bubble=bubble_count,wax=wax_count,wax_bubble=wax_bubble_count,normal=normal_count)


            
        





    



@api.route('/sums',methods=['GET','POST'])
def sums():
    index=[]
    sums=0
    for i in range(conn.llen(LIST_NAME))[10::-1]:
        real_time_data=str(conn.lindex(LIST_NAME,i),'utf-8')
        real_time_data=json.loads(real_time_data)       #反序列化,dict类型 
        state=get_state(real_time_data)
        if state =='start':
            index.append(0)
        elif state == 'complete':
            index.append(1)
        else:
            continue
                           
    return 'a'


@api.route('/test',methods=['GET','POST'])
def test():
    cars={'wash_time':123}
    conn.rpush('carlist',str(cars))
    return 'ok'




@api.route('/getData',methods=['GET','POST'])
def get_data():
    real_time_data=str(conn.lindex(LIST_NAME,0),'utf-8')
    real_time_data=json.loads(real_time_data)       #反序列化,dict类型 
    time=timestamp_to_normal_time(real_time_data['time'])
    return jsonify({'time':time})

@api.route('/screen',methods=['GET','POST'])
def screen():
    conn=connect_redis()
    real_time_data=str(conn.lindex(LIST_NAME,0),'utf-8')
    real_time_data=json.loads(real_time_data)       #反序列化,dict类型
    state={}
    if real_time_data['car_mode']=='car_washcomplete' and real_time_data['value']=='0':
        state['car']='start'
    if real_time_data['car_mode']=='car_washcomplete' and real_time_data['value']=='1':
        state['car']='complete'
    if real_time_data['car_mode']=='car_forward' and real_time_data['value']=='1':
        state['car']='start_forward'
    if real_time_data['car_mode']=='car_forward' and real_time_data['value']=='0':
        state['car']='finish_forward'
    if real_time_data['car_mode']=='car_in_pos' and real_time_data['value']=='1':
        state['car']='position_ok'
    if real_time_data['car_mode']=='car_back' and real_time_data['value']=='1':
        state['car']='start_back'
    if real_time_data['car_mode']=='car_back' and real_time_data['value']=='0':
        state['car']='finish_back'
    if real_time_data['car_mode']=='car_wash' and real_time_data['value']=='1':
        state['car']='start_wash'
    if real_time_data['car_mode']=='car_wash'and real_time_data['value']=='0':
        state['car']='finish_wash'
    if real_time_data['car_mode']=='car_bubble'and real_time_data['value']=='1':
        state['car']='start_bubble'
    if real_time_data['car_mode']=='car_bubble'and real_time_data['value']=='0':
        state['car']='finish_bubble'
    if real_time_data['car_mode']=='car_blow'and real_time_data['value']=='1':
        state['car']='start_blow'
    if real_time_data['car_mode']=='car_blow'and real_time_data['value']=='0':
        state['car']='finish_blow'
    if real_time_data['car_mode']=='car_wax'and real_time_data['value']=='1':
        state['car']='start_wax'
    if real_time_data['car_mode']=='car_wax'and real_time_data['value']=='0':
        state['car']='finish_wax'
    if real_time_data['car_mode']=='car_clean'and real_time_data['value']=='1':
        state['car']='push_water'
    if real_time_data['car_mode']=='car_clean'and real_time_data['value']=='0':
        state['car']='end_push'
    return jsonify(state)





# name=get_redis_data('name')
    # set_redis_data('sex','male')
    # sex=get_redis_data('sex')
    # s={"car_mode":"car-clean","value":"1","time":"1558678926415"}
    # data=json.dumps(s)
    # print(data,type(data))
    # conn=connect_redis()
    # conn.rpush('newlist','{"car_mode":"car-bubble","value":"0","time":"1558678926415"}')
    
    # j=conn.lrange('newlist',0,2)
    # print(j)
    # return sex


# if state=='start':
#         set_hash('washcars','all_time',real_time_data['time'])
#     elif state=='start_wash' and get_hash_if_exists('washcars','all_time') is not None:
#         set_hash('washcars',{'wash_time':real_time_data['time']})
#     elif state=='finish_wash' and flag==1:
#         start_time=conn.hget('washcars','wash_time')
#         difference=int(real_time_data['time'])-int(start_time)
#         wash_gap=timestamp_to_normal_time(difference)
#         set_hash('washcars','wash_time',wash_gap)
    
#     elif state=='start_bubble' and flag==1:
#         set_hash('washcars','bubble_time',real_time_data['time'])
#     elif state=='finish_bubble' and flag==1:
#         start_time=conn.hget('washcars','bubble_time')
#         difference=int(real_time_data['time'])-int(start_time)
#         bubble_gap=timestamp_to_normal_time(difference)
#         set_hash('washcars','bubble_time',bubble_gap)
#     elif state=='start_blow' and flag==1:
#         set_hash('washcars','blow_time',real_time_data['time'])
#     elif state=='finish_blow' and flag==1:
#         start_time=conn.hget('washcars','blow_time')
#         difference=int(real_time_data['time'])-int(start_time)
#         blow_gap=timestamp_to_normal_time(difference)
#         set_hash('washcars','blow_time',blow_gap)
#     elif state=='start_wax' and flag==1:
#         set_hash('washcars','wax_time',real_time_data['time'])
#     elif state=='finish_wax' and flag==1:
#         start_time=conn.hget('washcars','wax_time')
#         difference=int(real_time_data['time'])-int(start_time)
#         wax_gap=timestamp_to_normal_time(difference)
#         set_hash('washcars','wax_time',wax_gap)
#     elif state=='push_water' and flag==1:
#         set_hash('washcars','clean_time',real_time_data['time'])
#     elif state=='end_push' and flag==1:
#         start_time=conn.hget('washcars','clean_time')
#         difference=int(real_time_data['time'])-int(start_time)
#         clean_gap=timestamp_to_normal_time(difference)
#         set_hash('washcars','clean_time',clean_gap)
        
#     elif state=='complete' and :
        
#         start_time=get_hash_if_exists('washcars','all_time')
#         difference=int(real_time_data['time'])-int(start_time)
#         all_time=timestamp_to_normal_time(difference)
#         set_hash('washcars','all_time',all_time)
#         wash_time=get_hash_if_exists('washcars','wash_time')
#         bubble_time=get_hash_if_exists('washcars','bubble_time')
#         blow_time=get_hash_if_exists('washcars','blow_time')
#         wax_time=get_hash_if_exists('washcars','wax_time')
#         clean_time=get_hash_if_exists('washcars','clean_time')
#         #序列化字典存入redis列表.
#         #清空washcars哈希表。