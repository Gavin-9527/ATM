"""
数据处理层
    - 专门用户处理数据的
"""

# -*- coding:utf-8 -*-
import json
import os
from conf import settings
# 查看数据
def select(username):
    # 1)接收接口层传过来的username用户名，拼接用户json文件路径

    user_path = os.path.join(
        settings.USER_DATA_PATH, f'{username}.json'
    )
    # 2) 校验用户json文件是否存在
    if os.path.exists(user_path):
        # 打开数据，并返回给接口层
        with open(user_path, 'r', encoding='utf-8') as f:
            user_dic = json.load(f)
            return user_dic

    # 3) 不return，默认return None

# 保存数据（添加新数据或者更新数据）
def save(user_dic):
    username = user_dic['username']
    user_path = os.path.join(
        settings.USER_DATA_PATH, f'{username}.json'
    )
    with open(user_path, 'w', encoding='utf-8') as f:
        json.dump(user_dic, f, ensure_ascii=False)