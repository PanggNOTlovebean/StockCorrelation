import os
import pandas as pd 
import numpy as np
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties
import json
import baostock as bs

def get_stock_data(code, start_date, end_date):
    # 登陆系统
    bs.login()
    # 读取start_date至end_date期间的数据
    rs = bs.query_history_k_data_plus(
        code, "date,code,pctChg", start_date=start_date, end_date=end_date, frequency="d", adjustflag="3")
    # 将读取信息格式化处理，更改为PandasDataFrame对象
    data_list = []
    while (rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    result.rename(columns={'date': "Date",}, inplace=True)
    result["Date"] = result.apply(
        lambda x: datetime.datetime.strptime(x['Date'], "%Y-%m-%d"), axis=1)
    result.set_index('Date', inplace=True)
    # 登出系统
    bs.logout()
    return result

def main():
    # name_list=['上证指数', '中小板指', '创业板指', '区块链', '医药制造', '工业互联网', '数字货币', '深证成指', '白酒', '芯片', '蚂蚁金服']
    name_list=['白酒']
    
    start_date='2020-01-01'
    end_date='2020-10-01'
    
    for name in name_list:
        path= os.path.join('板块指数',name+'.csv')
        print(path)
        boss=pd.read_csv(path,encoding='utf-8')
        boss["Date"] = boss.apply(
        lambda x: datetime.datetime.strptime(x['Date'], "%Y-%m-%d"), axis=1)
        boss.set_index('Date',inplace=True)
        print(boss['2020'])
        path = os.path.join('板块个股代码',name+'.txt')

        with open(path) as fp:
            content=fp.readlines()
            for line in content:
                rs=get_stock_data(code=line[:-1],start_date=start_date,end_date=end_date)
        
    return

if __name__ == '__main__':
    main()