# 数据统计

data = '''评价ID,用户ID,评价时间,评价内容,评价星级
1,001,2021-01-01,很好，下次还会购买,5
2,002,2021-01-02,质量不错，物美价廉,4
3,003,2021-01-03,发货速度很快，值得信赖,5
4,001,2021-01-04,产品质量不错，物有所值,4
5,002,2021-01-05,客服服务态度不好，需要改进,2'''

lines = data.split('\n')  # 将原始数据按行分割

# 计算每个用户的平均评价星级
user_ratings = {}  # 用字典存储每个用户的评价信息
for line in lines[1:]:  # 遍历每一行数据，忽略第一行的列名
    values = line.split(',')  # 将行数据按逗号分割
    user_id = values[1]  # 获取用户ID
    rating = int(values[4])  # 获取评价星级
    user_ratings.setdefault(user_id, [])  # 如果用户ID不存在，则为其创建一个空列表
    user_ratings[user_id].append(rating)  # 将该用户的评价星级添加到列表中

user_avg_ratings = {}  # 用字典存储每个用户的平均评价星级
for user_id, ratings in user_ratings.items():
    user_avg_ratings[user_id] = sum(ratings) / len(ratings)

print('每个用户的平均评价星级：', user_avg_ratings)

# 计算所有用户的平均评价星级
avg_rating_all = sum(user_avg_ratings.values()) / len(user_avg_ratings)
print('所有用户的平均评价星级：', avg_rating_all)