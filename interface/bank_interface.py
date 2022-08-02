"""
银行相关业务的接口
"""
from db import db_handler
import time
# 提现接口(手续费5%)
def withdraw_interface(username, money):

    # 1) 先获取用户字典
    user_dic = db_handler.select(username)
    # 校验用户的钱是否足够
    balance = int(user_dic['balance'])
    # 提现本金加手续费
    money2 = int(money) * 1.005

    if balance >= money:

        # 2) 修改用户字典中的金额
        balance -= money2
        user_dic['balance'] = balance

        # 记录流水
        login_user_flow = time.strftime('%Y-%m-%d %H:%M:%S %p'), f'用户[{username}]提现[{money}]元成功,手续费为[{round((money2-float(money)),2)}]元。!'
        user_dic['flow'].append(login_user_flow)
        # 3) 再保存数据，或更新数据
        db_handler.save(user_dic)

        return True, login_user_flow

# 还款接口
def repay_interface(username, money):
    '''
    获取用户的金额
    给用户的金额做价钱操作
    :return:
    '''

    user_dic = db_handler.select(username)

    user_dic['balance'] += money

    # 记录流水
    login_user_flow = time.strftime('%Y-%m-%d %H:%M:%S %p'), f'用户[{username}]还款[{money}]元成功.'
    user_dic['flow'].append(login_user_flow)

    # 更新数据
    db_handler.save(user_dic)

    return True, login_user_flow

# 转账金额
def transfer_interface(login_user, to_user, money):
    login_user_dic = db_handler.select(login_user)

    to_user_dic = db_handler.select(to_user)

    # 判断目标用户是否存在
    if not to_user_dic:
        return False, '目标用户不存在。'

    # 判断是否为同一人：
    if login_user == to_user:
        return False, '不能给自己转账。'

    # 若目标用户存在，则判断 转账金额 是否足够。
    if login_user_dic['balance'] >= money:
        # 若足够，则开始转账
        login_user_dic['balance'] -= money

        to_user_dic['balance'] += money

        # 记录流水
        login_user_flow = time.strftime('%Y-%m-%d %H:%M:%S %p'), f'用户[{login_user}] 给用户[{to_user}] 转账 [{money}]元成功。'
        to_user_flow = time.strftime('%Y-%m-%d %H:%M:%S %p'), f'用户[{to_user}] 收到用户[{login_user}] 转账 [{money}]元成功。'

        login_user_dic['flow'].append(login_user_flow)
        to_user_dic['flow'].append(to_user_flow)

        # 保存用户数据
        db_handler.save(login_user_dic)
        db_handler.save(to_user_dic)

        return True, login_user_flow

    else:
        return False, '转账金额不足。'

# 查看流水接口
def check_flow_interface(login_user):
    user_dic = db_handler.select(login_user)
    return user_dic['flow']

# 结账购物车接口
def pay_interface(login_user, cost):

    user_dic = db_handler.select(login_user)


    if user_dic['balance'] >= cost:
        user_dic['balance'] -= cost

        flow = time.strftime('%Y-%m-%d %H:%M:%S %p'), f'用户消费金额：[{cost}]元 '
        user_dic['flow'].append(flow)
        user_dic['shop_car'] = {}

        db_handler.save(user_dic)
        return True
    return False