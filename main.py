import os
import pandas as pd 
import numpy as np
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties
import json
# 将相关性转化为排名
def numlist2ranklist(nums):
    args=np.argsort(1-np.array(nums,dtype=np.float32))

    result=np.zeros(len(args),dtype=np.int16)
    i=1
    for num in args:
        result[num]=i
        i=i+1
    return result

# 得到一个板块个股相关性变化的排名情况
def corr_rank(df):
    
    for index,row in df.iterrows():
        result=numlist2ranklist(df.loc[index].values)
        df.loc[index]=np.array(result,dtype=np.int16)
    return df

# 单只股票排名直方图
def rank_show(rank,name):
    xlen=len(rank.columns)
    sns.set(style="darkgrid")
    ax=sns.distplot(rank[name],bins=20,kde=False)
    ax.set_xlabel('rank')
    ax.set_ylabel('num')
    plt.show()

def corr_avg(df):
    df=df['2020']

    stock_corr_avg={}
    avg_list=[]
    for column in df.columns:
        avg=np.mean(df[column].values)
        stock_corr_avg[column]={}
        stock_corr_avg[column]['corr_avg']=avg
        avg_list.append(avg)
    
    ranks=numlist2ranklist(avg_list)
    
    i=0
    for column in df.columns:
        stock_corr_avg[column]['avg_rank']=ranks[i]
        stock_corr_avg[column]['best_corr']=np.max(df[column])
        stock_corr_avg[column]['worst_corr']=np.min(df[column])
        stock_corr_avg[column]['corr_range']=stock_corr_avg[column]['best_corr']-stock_corr_avg[column]['worst_corr']
        stock_corr_avg[column]['corr_std']=np.std(df[column].values)
        i=i+1
    df_rank=corr_rank(df)
    for column in df.columns:    
        stock_corr_avg[column]['best_rank']=np.min(df_rank[column])
        stock_corr_avg[column]['worst_rank']=np.max(df_rank[column])
        stock_corr_avg[column]['rank_range']=stock_corr_avg[column]['worst_rank']-stock_corr_avg[column]['best_rank']
    # result=pd.DataFrame(columns=['name','corr_avg','rank','best_corr','worst_corr','worst_corr','corr_range','best_rank','worst_rank','rank_range'])
    result=pd.DataFrame()
    for key in stock_corr_avg.keys():
        dict1={'name':key}
        dict1.update(stock_corr_avg[key])
        result=result.append(dict1,ignore_index=True)
    order=['name','corr_avg','avg_rank','best_corr','worst_corr','corr_range','corr_std','best_rank','worst_rank','rank_range']
    return result[order]

# 所有板块20日相关 排名情况
def run1():
    name_list=['上证指数.xlsx', '中小板指.xlsx', '创业板指.xlsx', '区块链.xlsx', '医药制造.xlsx', '工业互联网.xlsx', '数字货币.xlsx', '深证成指.xlsx', '白酒.xlsx', '芯片.xlsx', '蚂蚁金服.xlsx']
    for name in name_list:
        path=os.path.join('corr',name)
        df=pd.read_excel(path,sheet_name='20日相关性')
        df["date"] = df.apply(
        lambda x: datetime.datetime.strptime(x['date'], "%Y-%m-%d"), axis=1)
        df.set_index('date',inplace=True)
        df=df['2020']
        rank=corr_rank(df)
        newpath=os.path.join('corr_20_rank',name)
        rank.to_excel(newpath)

# 所有板块20日相关 平均值
def run2():
    name_list=['上证指数.xlsx', '中小板指.xlsx', '创业板指.xlsx', '区块链.xlsx', '医药制造.xlsx', '工业互联网.xlsx', '数字货币.xlsx', '深证成指.xlsx', '白酒.xlsx', '芯片.xlsx', '蚂蚁金服.xlsx']
    for name in name_list:
        path=os.path.join('corr',name)
        df=pd.read_excel(path,sheet_name='20日相关性')
        df["date"] = df.apply(
        lambda x: datetime.datetime.strptime(x['date'], "%Y-%m-%d"), axis=1)
        df.set_index('date',inplace=True)
        df=df['2020']
        result=corr_avg(df)
        result.to_excel(os.path.join('corr_20_all_result',name),encoding='gbk')
        
def main():
    name='白酒.xlsx'
    path=os.path.join('corr',name)

    df=pd.read_excel(path,sheet_name='20日相关性')
    df["date"] = df.apply(
    lambda x: datetime.datetime.strptime(x['date'], "%Y-%m-%d"), axis=1)
    df.set_index('date',inplace=True)
    df=df['2020']
    corr_avg(df)
    

            
if __name__ == "__main__":
    plt.rcParams['font.family'] = ['sans-serif']
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    # main()
    run2()