"""
逻辑接口层
    用户接口
"""
import json
import os
from conf import settings
from db import db_handler
from lib import common
user_logger = common.get_logger('user')
import time
# 注册接口

def register_interface(username, password, balance = 15000):
    # 2) 查看用户是否存在
    # 2.1) 调用 数据处理层 中的select函数，会返回字典或者None
    user_dic = db_handler.select(username)
    # 若用户存在，则return，告诉用户重新输入
    if user_dic:
        return False, '用户名已存在！'

    # 3) 若用户不存在，则保存用户数据
    # 做密码加密
    password = common.get_pwd_md5(password)
    # 3.1) 组织用户的数据的字典信息
    user_dic = {
        'username': username,
        'password': password,
        'balance': balance,
        # 用于记录用户流水的列表
        'flow': [],
        # 用于记录用户购物车
        'shop_car': {},
        # locked:用于记录用户是否被冻结
        # False:未冻结 True:已被冻结
        'locked': False,
    }

    # 记录流水
    user_flow = time.strftime('%Y-%m-%d %H:%M:%S %p'), f'{username} 注册成功。'
    user_dic['flow'].append(user_flow)
    # 3.2) 保存数据
    user_logger.info(user_flow)
    db_handler.save(user_dic)
    return True, user_flow

# 登录接口
def login_interface(username, password):

    # 1) 先查看当前用户数据是否存在
    user_dic = db_handler.select(username)
    # 判断用户是否存在
    if user_dic:
        # 判断用户是否被冻结
        if user_dic['locked']:
            return
        # 给用户输入的密码用一次加密
        password = common.get_pwd_md5(password)
        # 校验密码是否一致
        if password == user_dic['password']:
            msg = f'用户:[{username}] 登录成功！'
            user_logger.info(msg)
            return True, msg
        else:
            msg = '密码错误'
            user_logger.warn(msg)
            return False, msg

    return False, '用户不存在，请重新输入!'

# 查看余额接口
def check_bal_interface(username):
    user_dic = db_handler.select(username)
    return user_dic['balance']