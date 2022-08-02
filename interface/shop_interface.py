"""
购物商城接口
"""
from db import db_handler
from interface import bank_interface
# 结账购物车接口
def shopping_interface(login_user):
    user_dic = db_handler.select(login_user)

    if not user_dic['shop_car']:

        return False, '购物车为空，不能结账。'

    cost = 0
    for price, number in user_dic['shop_car'].values():
        cost += (price * number)


    flag = bank_interface.pay_interface(login_user, cost)

    if flag:
        return True, '支付成功，准备发货。'

    return False, '支付失败，金额不足。'

# 添加商品到购物车接口
def add_shop_car_interface(login_user, shopping_car):
    user_dic = db_handler.select(login_user)
    shop_car = user_dic['shop_car']
    for shop_name, price_number in shopping_car.items():
        number = price_number[1]
        if shop_name in shop_car:
            user_dic['shop_car'][shop_name][1] += number

        else:
            user_dic['shop_car'].update(
                {shop_name: price_number}
            )
    db_handler.save(user_dic)
    return True, '添加购物车成功。'

# 查看购物车接口
def check_car_interface(login_user):
    user_dic = db_handler.select(login_user)

    return user_dic['shop_car']
