#!/Users/lbs/Desktop/111/.venv/bin/python3

# 导入名为tushare的python库
import tushare as ts
# 导入datetime模块
import datetime
# 导入pandas模块
import pandas as pd
# 设置token
ts.set_token('a4589952c9262949c081834c03f3e729021f8a282b65497047f2162c')
# 初始化pro接口
pro = ts.pro_api()

# *********************************************日线行情备份接口的使用*********************************
# 特定日期范围，用于创建日期循环的参数，假如需要指定的日期就把这个逻辑注释掉，直接填写在接口body的地方。
start_date = "20250315"
end_date = "20250320"

# 创建空DataFrame用于存储结果
all_results = pd.DataFrame()

# 生成日期范围
date_range = pd.date_range(start=start_date, end=end_date)

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
        "close"
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
    all_results.to_csv('~/Desktop/bak_daily_all.csv', index=False)
    print("所有数据已成功保存为 CSV 文件！")
else:
    print("未获取到任何数据")


'''
# *********************************************龙虎榜每日明细接口的使用*********************************
# 龙虎榜每日明细，每天只能访问这个接口两次
df2 = pro.hm_detail(**{
    "trade_date": "20250328",
    "ts_code": "",
    "hm_name": "",
    "start_date": "",
    "end_date": "",
    "limit": "",
    "offset": ""
}, fields=[
    "trade_date",
    "ts_code",
    "ts_name",
    "buy_amount",
    "sell_amount",
    "net_amount",
    "hm_name"
])
# 将数据保存到CSV文件
df2.to_csv('~/Desktop/hm_detail.csv', index=False)
# 打印提示信息
print("hm_detail 数据已成功保存为 CSV 文件！")
'''