# 预测算法

# We can use linear regression to predict the next month's sales based on the existing data.

# First, we need to import the necessary libraries
import pandas as pd
from sklearn.linear_model import LinearRegression

# Next, we can create a dataframe with the existing sales data
sales_data = pd.DataFrame({'date': ['2021-01', '2021-02', '2021-03', '2021-04', '2021-05'],
                           'sales': [1000, 1500, 2000, 3500, 4000]})

# We need to convert the date column to a datetime object
sales_data['date'] = pd.to_datetime(sales_data['date'])

# We can then extract the month as a separate column
sales_data['month'] = sales_data['date'].dt.month

# We can now fit a linear regression model to the data
model = LinearRegression()
model.fit(sales_data[['month']], sales_data['sales'])

# Finally, we can predict the sales for the next month
next_month = pd.DataFrame({'month': [6]})
predicted_sales = model.predict(next_month)

# The predicted sales for the next month can be printed as follows
print(predicted_sales[0])

"""


# 定义销售数据
sales = {'2021-01': 1000,
         '2021-02': 1500,
         '2021-03': 2000,
         '2021-04': 3500,
         '2021-05': 4000}

# 计算平均值
last_3_sales = list(sales.values())[-3:]
forecast_sale = sum(last_3_sales) / len(last_3_sales)

# 输出预测值
print('The forecasted sale for next month is:', forecast_sale)
"""