"""
存放配置信息
"""

import os

# 获取项目根目录路径
BASE_PATH = os.path.dirname(
    os.path.dirname(__file__))

# 获取user_data文件夹目录路径
USER_DATA_PATH = os.path.join(
    BASE_PATH, 'db', 'user_data'
)



# 定义三种日志输出格式开始
standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]'\
                  '[%(levelname)s][%(message)s]' # 其中name为getlogger指定的名字
simple_format = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'

id_simple_format = '[%(levelname)s][%(asctime)s] %(message)s'
# 定义日志输出格式 结束
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
logfile_dir = os.path.join(BASE_DIR, 'log')  # log文件的目录
logfile_name = 'atm.log'  # log文件名

# 如果不存在定义的日志目录就创建一个
if not os.path.isdir(logfile_dir):
    os.mkdir(logfile_dir)

# log文件的全路径
logfile_path = os.path.join(logfile_dir, logfile_name)

# log配置字典
LOGGING_DIC = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': standard_format
        },
        'simple': {
            'format': simple_format
        },
        'id_simple': {
            'format': id_simple_format
        },
    },
    'filters': {},
    # handlers是日志的接收者，不同的handler会将日志输出到不同的位置
    'handlers': {
        # 打印到终端的日志
        'stream': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',  # 打印到屏幕
            'formatter': 'simple'
        },
        # 打印到文件的日志,收集info及以上的日志
        'access': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',  # 轮转保存到文件，若为FileHandler则只是普通保存到未见
            'formatter': 'standard',
            # 可以定制日志文件路径
            # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            # LOG_PATH = os.path.join(BASE_DIR,'a1.loh')
            'filename': logfile_path,  # 日志文件
            'maxBytes': 1024*1024*5,  # 日志大小 5M
            'backupCount': 5,  # 若为轮转，则表示最多保存几份文件，多则删除
            'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
        },
        # 打印到文件的日志,收集error及以上的日志
        'boss': {
                    'level': 'ERROR',
                    'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
                    'formatter': 'id_simple',
                    'filename': logfile_name,  # 日志文件
                    # 'maxBytes': 1024*1024*5,  # 日志大小 5M
                    'maxBytes': 300,  # 日志大小 5M
                    'backupCount': 5,
                    'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
                },
    },
    # loggers是日志的产生者，产生的日志会传递给handler然后控制输出
    'loggers': {
        # logging.getLogger(__name__)拿到的logger配置
        'aaa': {
            'handlers': ['stream', 'access','boss'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
            'level': 'DEBUG',
            'propagate': False,  # 默认为True， 向上（更高level的logger）传递
        },
        'bbb': {
            'handlers': ['stream', 'access','boss'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
            'level': 'DEBUG',
            'propagate': False,  # 默认为True， 向上（更高level的logger）传递
        },
        # 若为空,logger若找不到其他logger的话可以取任意名
        '': {
            'handlers': ['stream', 'access'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
            'level': 'DEBUG',
            'propagate': False,  # 默认为True， 向上（更高level的logger）传递
        },
        # 这样我们再取logger对象时logging.getLogger(__name__)，不同的文件__name__不同，这保证了打印日志时标识信息不同，
        # 但是拿着该名字去loggers里找key名时却发现找不到，于是默认使用key=''的配置
    },
}

