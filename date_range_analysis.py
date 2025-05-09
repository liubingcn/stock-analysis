#!/usr/bin/env python3
# 导入必要的模块
import tushare as ts
import pandas as pd
import datetime
from config import API_TOKEN

# 获取当前时间戳
current_time = datetime.datetime.now().strftime('%Y%m%d')

# 全局配置和初始化
ts.set_token(API_TOKEN)
pro = ts.pro_api()

# 共享的日期配置
start_date = "20241007"
end_date = "20241008"
date_range = pd.date_range(start=start_date, end=end_date)

# *********************************************DF1_日线行情备份接口的使用*********************************
# 特定日期范围，用于创建日期循环的参数，假如需要指定的日期就把这个逻辑注释掉，直接填写在接口body的地方。
# 创建中文表头映射
column_mapping = {
    "ts_code": "股票代码",
    "trade_date": "交易日期",
    "name": "股票名称",
    "pct_change": "涨跌幅",
    "close": "收盘价",
    "vol_ratio": "量比",
    "turn_over": "换手率"
}

# 创建空DataFrame用于存储结果
all_results = pd.DataFrame()

# 遍历每个日期
for date in date_range:
    trade_date = date.strftime('%Y%m%d')
    print(f"正在处理日期: {trade_date}")
    
    # 获取日线备份行情数据
    df1 = pro.bak_daily(**{
        "ts_code": "",
        "trade_date": trade_date,
        "start_date": "",
        "end_date": "",
        "offset": "",
        "limit": ""
    }, fields=[
        "ts_code",
        "trade_date",
        "name",
        "pct_change",
        "close",
        "vol_ratio",
        "turn_over"
    ])

# 将pct_change转换为百分比格式
    if not df1.empty:
        df1['pct_change'] = df1['pct_change'].apply(lambda x: f"{x/100:.2%}")
    # 检查是否有数据
    if df1.empty:
        print(f"日期 {trade_date} 未查到数据")
    else:
        # 将当前日期的数据添加到结果集中
        all_results = pd.concat([all_results, df1], ignore_index=True)
        print(f"日期 {trade_date} 数据已成功获取")

# 将所有结果保存到CSV文件
if not all_results.empty:
    # 重命名列
    all_results = all_results.rename(columns=column_mapping)
    # 使用时间戳生成文件名
    filename = f'日线行情连续_{current_time}.csv'
    # 保存到CSV文件
    all_results.to_csv(f'~/Desktop/{filename}', index=False)
    print(f"所有数据已成功保存为 {filename}")
else:
    print("未获取到任何数据")

