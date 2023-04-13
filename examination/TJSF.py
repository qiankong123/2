# 8推荐算法

"""
# Create a dictionary to store the purchase history of each user
purchase_history = {
    '001': ['A001', 'A002', 'A003'],
    '002': ['A001', 'A004', 'A005'],
    '003': ['A002', 'A003', 'A006']
}

# Create a dictionary to store the similarity score between each item
item_similarity = {
    'A001': {'A002': 0.5, 'A003': 0.3, 'A004': 0.1, 'A005': 0.2, 'A006': 0.1},
    'A002': {'A001': 0.5, 'A003': 0.4, 'A004': 0.2, 'A005': 0.1, 'A006': 0.3},
    'A003': {'A001': 0.3, 'A002': 0.4, 'A004': 0.1, 'A005': 0.2, 'A006': 0.2},
    'A004': {'A001': 0.1, 'A002': 0.2, 'A003': 0.1, 'A005': 0.3, 'A006': 0.4},
    'A005': {'A001': 0.2, 'A002': 0.1, 'A003': 0.2, 'A004': 0.3, 'A006': 0.2},
    'A006': {'A001': 0.1, 'A002': 0.3, 'A003': 0.2, 'A004': 0.4, 'A005': 0.2}
}

# Define a function to recommend items for a given user
def recommend_items(user_id, n):
    # Get the purchase history of the user
    purchased_items = purchase_history[user_id]
    # Create a dictionary to store the similarity score between each item and the purchased items
    similarity_scores = {}
    for item in item_similarity:
        if item not in purchased_items:
            similarity_scores[item] = sum([item_similarity[item][purchased_item] for purchased_item in purchased_items if purchased_item in item_similarity[item]])
    return  similarity_scores
    # Sort the similarity scores in descending order

print(recommend_items('001',1))
"""

"""
import pandas as pd
import numpy as np
from itertools import combinations
from collections import defaultdict

# 构建商品-用户倒排表
def build_user_item_dict(data):
    user_item = defaultdict(list)
    for index, row in data.iterrows():
        user_item[row['商品ID']].append(row['用户ID'])
    return user_item

# 计算余弦相似度
def cosine_sim(a, b):
    cos_sim = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    return cos_sim

# 计算商品之间的相似度
def compute_item_sim(user_item):
    item_sim = defaultdict(defaultdict)
    for item_pair in combinations(user_item.keys(), 2):
        itemA, itemB = item_pair
        users_A = set(user_item[itemA])
        users_B = set(user_item[itemB])
        common_users = users_A & users_B
        if len(common_users) == 0: # 如果两个商品没有共同的用户购买过，则相似度为0
            sim = 0
        else:
            users_A_dict = {u: 1 for u in users_A}
            users_B_dict = {u: 1 for u in users_B}
            a = [users_A_dict.get(u, 0) for u in common_users]
            b = [users_B_dict.get(u, 0) for u in common_users]
            sim = cosine_sim(a, b)
        item_sim[itemA][itemB] = sim
        item_sim[itemB][itemA] = sim
    return item_sim

# 推荐相似度最高的前N个商品
def recommend_items(user, user_item, item_sim, topN):
    purchased_items = user_item[user]
    item_scores = defaultdict(float)
    for item in user_item.keys():
        if item not in purchased_items:
            for purchased_item in purchased_items:
                item_scores[item] += item_sim[purchased_item][item]
    sorted_items = sorted(item_scores.items(), key=lambda x:x[1], reverse=True)[:topN]
    return [x[0] for x in sorted_items]

# 测试数据
data = pd.DataFrame({'用户ID': ['001', '001', '001', '002', '002', '002', '003', '003', '003'],
                     '商品ID': ['A001', 'A002', 'A003', 'A001', 'A004', 'A005', 'A002', 'A003', 'A006'],
                     '购买时间': ['2021-01-01', '2021-01-02', '2021-01-03', '2021-01-04', '2021-01-05', '2021-01-06', '2021-01-07', '2021-01-08', '2021-01-09']})

# 构建商品-用户倒排表
user_item = build_user_item_dict(data)

# 计算商品之间的相似度
item_sim = compute_item_sim(user_item)

# 推荐相似度最高的前N个商品
topN = 2
for user in user_item.keys():
    recommended_items = recommend_items(user, user_item, item_sim, topN)
    print(f'用户{user}的推荐结果是{recommended_items}')  # 用户001的推荐结果是['A006', 'A004'] 用户002的推荐结果是['A006', 'A002'] 用户003的推荐结果是['A001', 'A004']
    
"""


import math

# 用户购买记录
data = [
    {'user_id': '001', 'goods_id': 'A001', 'buy_time': '2021-01-01'},
    {'user_id': '001', 'goods_id': 'A002', 'buy_time': '2021-01-02'},
    {'user_id': '001', 'goods_id': 'A003', 'buy_time': '2021-01-03'},
    {'user_id': '002', 'goods_id': 'A001', 'buy_time': '2021-01-04'},
    {'user_id': '002', 'goods_id': 'A004', 'buy_time': '2021-01-05'},
    {'user_id': '002', 'goods_id': 'A005', 'buy_time': '2021-01-06'},
    {'user_id': '003', 'goods_id': 'A002', 'buy_time': '2021-01-07'},
    {'user_id': '003', 'goods_id': 'A003', 'buy_time': '2021-01-08'},
    {'user_id': '003', 'goods_id': 'A006', 'buy_time': '2021-01-09'},
]

# 将用户购买记录转换成为每个用户购买的商品集合
user_goods = {}
for d in data:
    user_id = d['user_id']
    goods_id = d['goods_id']
    if user_id not in user_goods:
        user_goods[user_id] = set()
    user_goods[user_id].add(goods_id)

# 统计每个商品被多少用户购买
goods_buy_users = {}
for user_id, goods_set in user_goods.items():
    for goods_id in goods_set:
        if goods_id not in goods_buy_users:
            goods_buy_users[goods_id] = set()
        goods_buy_users[goods_id].add(user_id)

# 计算两个商品之间的余弦相似度
def cosine_sim(goods1, goods2):
    # 计算交集
    intersection = goods1 & goods2
    # 如果交集为空，则两个商品之间相似度为0
    if len(intersection) == 0:
        return 0
    # 计算两个商品之间的相似度
    return len(intersection) / math.sqrt(len(goods1) * len(goods2))

# 计算每个商品与其他所有商品之间的相似度，保存到一个字典中
goods_sim = {}
for goods_id1, users1 in goods_buy_users.items():
    goods_sim[goods_id1] = {}
    goods1 = users1
    for goods_id2, users2 in goods_buy_users.items():
        if goods_id1 == goods_id2:
            continue
        goods2 = users2
        sim = cosine_sim(goods1, goods2)
        goods_sim[goods_id1][goods_id2] = sim

# 推荐算法，根据相似度列表推荐前N个商品
def recommend(user_id, N=10):
    # 获取用户购买的商品集合
    user_goods_set = user_goods[user_id]
    # 定义一个字典保存每个商品的相似度得分
    goods_score = {}
    # 遍历每个商品，计算它与用户未购买的商品之间的相似度得分
    for goods_id1 in user_goods_set:
        for goods_id2, sim in goods_sim[goods_id1].items():
            if goods_id2 in user_goods_set:
                continue
            if goods_id2 not in goods_score:
                goods_score[goods_id2] = 0
            goods_score[goods_id2] += sim
    # 将推荐结果按照相似度得分排序并返回前N个结果
    sorted_goods = sorted(goods_score.items(), key=lambda x: x[1], reverse=True)[:N]
    return [goods_id for goods_id, score in sorted_goods]

# 测试推荐算法
for user_id in user_goods.keys():
    print(f'user {user_id} recommend goods:', recommend(user_id))
