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
input_date = "20250407"
# 如果用户没有输入日期，则使用当前日期
if not input_date:
    input_date = datetime.datetime.now().strftime('%Y%m%d')
# 验证日期格式
if len(input_date) != 8 or not input_date.isdigit():
    print("日期格式不正确，请输入8位数字（YYYYMMDD）")
    exit(1)
'''
# *********************************************DF1_日线行情备份接口的使用*************************************************
# 日线行情备份接口，每天可以调用多次
df1 = pro.bak_daily(**{
    "ts_code": "",
    "trade_date": input_date,        
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

# 检查是否获取到数据
if df1.empty:
    print(f"日期 {input_date} 未查到数据")
else:
    print(f"日期 {input_date} 数据已成功获取")
    
# 创建中文表头映射
column_mapping = {
    "trade_date": "交易日期",
    "ts_code": "股票代码",
    "name": "股票名称",
    "pct_change": "涨跌幅",
    "close": "收盘价",
    "vol_ratio": "量比",
    "turn_over": "换手率"
}

# 将pct_change转换为百分比格式
df1['pct_change'] = df1['pct_change'].apply(lambda x: f"{x/100:.2%}")

try:
    # 将数据保存到CSV文件
    # 先将数据列重命名，然后保存
    df1_renamed = df1.rename(columns=column_mapping)
    df1_renamed.to_csv('~/Desktop/bak_daily.csv', index=False, encoding='utf-8-sig')
    print("bak_daily 数据已成功保存为 CSV 文件！")
except Exception as e:
    print(f"保存CSV文件时出错: {str(e)}")
    print("未获取到任何数据")
'''
# *********************************************DF2_大盘资金流向接口的使用*************************************************
# 大盘资金流向接口，每天可以调用多次
df2 = pro.moneyflow_mkt_dc(**{
    "trade_date": input_date,
    "start_date": "",# 开始日期
    "end_date": "",# 结束日期
    "limit": "",# 单次返回数据长度
    "offset": ""# 请求数据的开始位移量
}, fields=[
    "trade_date",
    "net_amount",# 今日主力净流入净额（元）
    "buy_elg_amount",# 今日超大单净流入净额（元）
    "buy_lg_amount",# 今日大单净流入净额（元）
    "buy_md_amount",# 今日中单净流入净额（元）
    "buy_sm_amount"# 今日小单净流入净额（元）
])

# 检查是否获取到数据
if df2.empty:
    print(f"日期 {input_date} 未查到数据")
else:
    print(f"日期 {input_date} 数据已成功获取")
    
# 创建中文表头映射
column_mapping = {
    "trade_date": "交易日期",
    "net_amount": "主力净流入净额",
    "buy_elg_amount": "超大单净流入净额",
    "buy_lg_amount": "大单净流入净额",
    "buy_md_amount": "中单净流入净额",
    "buy_sm_amount": "小单净流入净额"
}
# 将数据的单位从"元"转化为"亿"
df2['net_amount'] = df2['net_amount'].apply(lambda x: x / 100000000)
df2['buy_elg_amount'] = df2['buy_elg_amount'].apply(lambda x: x / 100000000)
df2['buy_lg_amount'] = df2['buy_lg_amount'].apply(lambda x: x / 100000000)
df2['buy_md_amount'] = df2['buy_md_amount'].apply(lambda x: x / 100000000)
df2['buy_sm_amount'] = df2['buy_sm_amount'].apply(lambda x: x / 100000000)

try:
    # 将数据保存到CSV文件
    # 先将数据列重命名，然后保存
    df2_renamed = df2.rename(columns=column_mapping)
    df2_renamed.to_csv('~/Desktop/fund_flow.csv', index=False, encoding='utf-8-sig')
    print("fund_flow 数据已成功保存为 CSV 文件！")
except Exception as e:
    print(f"保存CSV文件时出错: {str(e)}")
    print("未获取到任何数据")