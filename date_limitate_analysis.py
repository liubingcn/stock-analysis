#!/usr/bin/env python3

# 导入名为tushare的python库
import tushare as ts
# 导入pandas模块
import pandas as pd
# 导入 datetime 模块
import datetime
# 导入配置文件
from config import API_TOKEN
# 设置token
ts.set_token(API_TOKEN)
# 初始化pro接口
pro = ts.pro_api()
# 指定的查询日期
input_date = "20250403"
# 如果用户没有输入日期，则使用当前日期
if not input_date:
    input_date = datetime.datetime.now().strftime('%Y%m%d')
# 验证日期格式
if len(input_date) != 8 or not input_date.isdigit():
    print("日期格式不正确，请输入8位数字（YYYYMMDD）")
    exit(1)

# *********************************************DF1_龙虎榜接口的使用*************************************************
# 龙虎榜接口，每天只能调用2次
df1 = pro.hm_detail(**{
    "trade_date": input_date,
    "ts_code": "",# 股票代码
    "hm_name": "",# 游资名称
    "start_date": "",# 开始日期
    "end_date": "",# 结束日期
    "limit": "",# 单次返回数据长度
    "offset": ""# 请求数据的开始位移量
}, fields=[
    "trade_date",
    "ts_code",
    "ts_name",
    "buy_amount",
    "sell_amount",
    "net_amount",
    "hm_name"
])

# 检查是否获取到数据
if df1.empty:
    print(f"日期 {input_date} 未查到数据")
else:
    print(f"日期 {input_date} 数据已成功获取")
    
# 创建中文表头映射
column_mapping = {
    "trade_date": "交易日期",
    "ts_code": "股票代码",
    "ts_name": "股票名称",
    "buy_amount": "买入金额",
    "sell_amount": "卖出金额",
    "net_amount": "净额",
    "hm_name": "龙虎榜名称"
}

try:
    # 将数据保存到CSV文件
    # 先将数据列重命名，然后保存
    df1_renamed = df1.rename(columns=column_mapping)
    df1_renamed.to_csv('~/Desktop/hm_detail.csv', index=False, encoding='utf-8-sig')
    print("hm_detail 数据已成功保存为 CSV 文件！")
except Exception as e:
    print(f"保存CSV文件时出错: {str(e)}")
    print("未获取到任何数据")
