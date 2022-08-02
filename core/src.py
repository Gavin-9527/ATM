"""
用户视图层
"""
from interface import user_interface
from interface import bank_interface
from interface import  shop_interface
from lib import common
import time
# 全局变量，记录用户是否已登录
login_user = None
# 1、注册
# 面条版
'''def register():
    while True:
        # 1) 让用户输入用户名与密码进行校验
        username = input('请输入用户名:').strip()
        password = input('请输入密码:').strip()
        re_password = input('请确认密码:').strip()

        # 2) 小的逻辑处理:比如两次密码是否一致
        if password == re_password:

            # 接收到注册之后的结果并打印
            # 2) 查看用户是否存在
            import json
            import os
            from conf import settings
            user_path = os.path.join(
                settings.USER_DATA_PATH, f'{username}.json'
            )
            # 3) 若用户存在，则让用户重新输入
            if os.path.exists(user_path):
                print('用户已存在，请重新输入！')
                continue
            # 4) 若用户不存在，则保存用户数据
            with open(user_path, 'r', encoding='utf-8') as f:
                json.dump(user_dic, f)



            # 4.1) 组织用户的数据的字典信息
            user_dic = {
                'username': username,
                'password': password,
                'balance': 15000,
                # 用于记录用户流水的列表
                'flow': [],
                # 用于记录用户购物车
                'shop_car':{},
                # locked:用于记录用户是否被冻结
                # False:未冻结 True:已被冻结
                'locker': False
            }
            import json
            import os
            from conf import settings
            # 用户数据，以名字取文件名
            # 4.2)拼接用户的json文件路径
            user_path = os.path.join(
                settings.USER_DATA_PATH, f'{username}.json'
            )
            with open(user_path, 'w', encoding='utf-8') as f:
                json.dump(user_dic, f)

            pass
    pass'''

# 分层板

def register():
    while True:
        # 1) 让用户输入用户名与密码进行校验
        username = input('请输入用户名:').strip()
        password = input('请输入密码:').strip()
        re_password = input('请确认密码:').strip()
        # 可以输入自定义的金额
        #  小的逻辑处理:比如两次密码是否一致
        if password == re_password:
            # 2) 调用接口层的注册接口，将用户名和密码交给接口层来处理
            # (True,用户注册成功), (False,注册失败)
            flag, msg = user_interface.register_interface(username, password)
            # 3) 根据flag查看是否创建成功,成功则跳出注册
            if flag:
                print(msg)
                break
            else:
                print(msg)
        else:
            print('两次密码不一样，请重新输入!')
# 2、登录

def login():
    while True:
        username = input('请输入用户名：').strip()
        password = input('请输入密码：').strip()
        # 调用接口层，将数据传给登录接口
        flag, msg = user_interface.login_interface(username, password)
        if flag:
            print(msg)
            global login_user
            login_user = username
            break
        else:
            print(msg)


# 3、查看余额
@common.login_auth
def check_balance():
    # 直接调用查看余额接口，获取用户余额
    balance = user_interface.check_bal_interface(login_user)

    print(f'用户{login_user} 账户余额为: {balance}')

# 4、提现
@common.login_auth
def withdraw():
    while True:

        # 1)让用户输入提现金额
        input_money = input('请输入提现金额:').strip()

        # 2)判断用户输入的金额是否时数字
        if not input_money.isdigit():
            print('请重新输入。')
            continue

        # 3)用户提现金额，将提现的金额交付给接口层来处理
        input_money = int(input_money)
        flag, msg = bank_interface.withdraw_interface(
            login_user, input_money
        )

        if flag:
            print(msg)
            break
        else:
            print(msg)
    pass

# 5、还款
@common.login_auth
def repay():

    '''
    银行卡还款，无论是信用卡或储蓄卡，能冲任意大小的金额
    :return:
    '''
    # 让用户输入还款金额
    while True:
        input_money = input('请输出还款的金额：').strip()
        # 判断用户输入的是否时数字
        if not input_money.isdigit():
            print('请输入正确的金额。')
            continue
        input_money = int(input_money)

        if input_money > 0:
            flag, msg = bank_interface.repay_interface(
                login_user, input_money
            )
            if flag:
                print(msg)
                break
        else:
            print('输入的金额不可以小于0,请重新输入。')
            continue

# 6、转账
@common.login_auth
def transfer():
    '''
    接收 转账目标用户
    接收 转账金额
    :return:
    '''
    while True:
        to_user = input('请输入转账目标用户:').strip()
        money = input('请输入转账金额:').strip()

        if not money.isdigit():
            print('请输入正确的金额！')
            continue
        money = int(money)

        if money > 0:
            flag, msg = bank_interface.transfer_interface(
                login_user, to_user, money
            )
            if flag:
                print(msg)
                break
            else:
                print(msg)
        else:
            print('请输入大于零的金额。')

# 7、查看流水
@common.login_auth
def check_flow():
    flow_list = bank_interface.check_flow_interface(
        login_user
    )

    if flow_list:
        for flow in flow_list:
            print(flow)
    else:
        print('当前用户没有流水。')

# 8、购物
@common.login_auth
def shopping():
    # 不从文件中读取商品，这里直接写
    # 商品列表
    shop_list = [
        ['上海灌汤包', 30],
        ['xzk公仔', 60],
        ['xjw煲仔饭', 250],
        ['香蕉', 10],
        ['鱼香肉丝',20]
    ]
    # 初始化当前购物车
    shopping_car = {} #{'shop_name':'shop_price','num'}

    while True:
        # 枚举:enumerate(可迭代对象)  ---->(可迭代对象的索引，索引对应的值)
        # 枚举:enumerate(可迭代对象)  ---->(0，['上海灌汤包',30])
        for index, shop in enumerate(shop_list):
            print(f'商品编号为：[{index}],',
                  f'商品名称为：[{shop[0]}],',
                  f'商品单价为：[{shop[1]}]元')

        choice = input('请输入商品编号(是否结账输入y or n):').strip()

        if choice == 'y':

            flag, msg = shop_interface.shopping_interface(login_user)
            if flag:
                print(msg)
                break
            else:
                print(msg)


        elif choice == 'n':
            if not shopping_car:
                print('购物车是空的，不能添加，请重新输入。')
                continue

            flag, msg = shop_interface.add_shop_car_interface(
                login_user, shopping_car
            )
            if flag:
                print(msg)
                break

        if not choice.isdigit():
            print('请输入正确的编号。')
            continue
        choice = int(choice)

        if choice not in range(len(shop_list)):
            print('请输入正确的编号。')
            continue
        shop_name, shop_price = shop_list[choice]

        # 加入购物车
        if shop_name in shopping_car:
            shopping_car[shop_name][1] += 1
        else:
            shopping_car[shop_name] = [shop_price, 1]
    pass

# 9、查看购物车
@common.login_auth
def check_shop_car():
    shop_car = shop_interface.check_car_interface(login_user)
    if shop_car:
        for index, shop in shop_car.items():
            print(f'购物车商品[{index}],',
                  f'单价[{shop[0]}],',
                  f'数量[{shop[1]}]。')




# 10、管理员功能
@common.login_auth
def admin():
    from core import admin
    admin.admin_run()

# 创建函数功能字典
func_dic = {
    '0': exit,
    '1': register,
    '2': login,
    '3': check_balance,
    '4': withdraw,
    '5': repay,
    '6': transfer,
    '7': check_flow,
    '8': shopping,
    '9': check_shop_car,
    '10': admin,
    }
# 视图层主程序
def run():
    while True:
        print(
             time.strftime('%Y-%m-%d %H:%M:%S %p').center(40,'-')
        )
        print(
            '''
        ==== ATM + 购物车 ====
            0、退出
            1、注册
            2、登录
            3、查看余额
            4、提现
            5、还款
            6、转账
            7、查看流水
            8、购物
            9、查看购物车
            10、管理员功能
        ======== end ========
        ''')

        choice = input('请输入功能编号:'.strip())

        if choice not in func_dic:
            print('请输入正确的功能编号!')
            continue
        func_dic[choice]()  # func_dic.get('1')() ---> register()
