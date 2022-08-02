from db import db_handler

# 修改额度接口
def change_balance_interface(username, money):
    user_dic = db_handler.select(username)

    if user_dic:
        user_dic['balance'] = int(money)

        db_handler.save(user_dic)

        return True, '额度修改成功'
    return False, '修改额度的用户不存在。'

# 冻结账户接口
def lock_user_interface(username):
    user_dic = db_handler.select(username)
    if user_dic:
        if user_dic['locked']:
            return False, '该用户已被冻结'
        db_handler.save(user_dic)

        return True, f'用户{username}账户冻结成功。'

    return False, f'用户{username}不存在。'