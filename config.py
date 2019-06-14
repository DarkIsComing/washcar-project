# REDIS_DB_URL_LOCAL = {
#         'host': '127.0.0.1',
#         'port': 6379,
#         'password': '',
#         'db': 0
#     }

REDIS_DB_URL_PRODUCE = {
    'host': 'mq.oakiot.com',
    'port':23226,
    'password': 'q0N9C5uldNe9sL0h27mt',
    'db': 15
}

LIST_NAME='washTec_77000059'
debug=True

SCHEDULER_API_ENABLED=True

#每天的零点定时启动app.api_1_0.views里的指定函数。
JOBS = [
    {
        'id': 'yesterday_data',
        'func': 'app.api_1_0.utils:update_yesterday_data',
        'args'  : '',
        'trigger': 'cron',
        'month' : '1-12',
        'day_of_week' : '0-6',
        'hour' : '0',
        'minute' : '0',
        'second' : "0"
    },
    {
        'id': 'test1',
        'func': 'app.api_1_0.utils:test1',
        'args'  : '',
        'trigger': 'cron',
        'month' : '1-12',
        'day_of_week' : '0-6',
        'hour' : '13',
        'minute' : '52',
        'second' : "0"
    },
    {
        'id': 'test2',
        'func': 'app.api_1_0.utils:test2',
        'args'  : '',
        'trigger': 'cron',
        'month' : '1-12',
        'day_of_week' : '0-6',
        'hour' : '13',
        'minute' : '52',
        'second' : "0"
    }
]