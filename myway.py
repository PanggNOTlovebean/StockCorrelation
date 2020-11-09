import os
import pandas as pd 
import numpy as np
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties
import json

def rank2score(max_num=100000,beta=0.98):
    score=np.linspace(start=1,stop=max_num,num=max_num)

    for i in range(max_num):
        if(i==0):
            continue
        score[i]=beta*score[i-1]+(1-beta)*score[i]
    return score

def rank_stastic(name,sigma=0.7):
    path=os.path.join('corr_20_rank',name)
    dt=pd.read_excel(path)
    max_rank=len(dt.columns)-1
    result_set={}
    scores=[]
    for column in dt.drop('date',axis=1).columns:
        ranks=dt[column].values
        ranks=np.sort(ranks)
        nb_ranks=ranks[:int(len(ranks)*sigma)]        
        sum_score=0
        for rank in nb_ranks:
            sum_score=sum_score+max_rank-rank+1
        result_set[column]={}
        result_set[column]['score']=sum_score
        scores.append(sum_score)
    stock_rank=numlist2ranklist(scores)
    MAX=np.max(scores)
    MIN=np.min(scores)
    i=0
    for column in dt.drop('date',axis=1).columns:
        result_set[column]['normal_score']=(result_set[column]['score']-MIN)/(MAX-MIN)
        result_set[column]['rank']=stock_rank[i]
        i=i+1
    result_df=pd.DataFrame(columns=['name','score','normal_score','rank'])
    for key in result_set.keys():
        result_df=result_df.append({'name':key,'score':result_set[key]['score'],'normal_score':result_set[key]['normal_score'],'rank':result_set[key]['rank'],},ignore_index=True)
    return result_df

def numlist2ranklist(nums):
    args=np.argsort(1-np.array(nums,dtype=np.float32))

    result=np.zeros(len(args),dtype=np.int16)
    i=1
    for num in args:
        result[num]=i
        i=i+1
    return result

def run1():
    name_list=['上证指数.xlsx', '中小板指.xlsx', '创业板指.xlsx', '区块链.xlsx', '医药制造.xlsx', '工业互联网.xlsx', '数字货币.xlsx', '深证成指.xlsx', '白酒.xlsx', '芯片.xlsx', '蚂蚁金服.xlsx']
    # name_list=['白酒.xlsx']
    for name in name_list:
        path=os.path.join('corr',name)
        df=pd.read_excel(path,sheet_name='20日相关性')
        df["date"] = df.apply(
        lambda x: datetime.datetime.strptime(x['date'], "%Y-%m-%d"), axis=1)
        df.set_index('date',inplace=True)
        df=df['2020']
        for index,row in df.iterrows():
            result=numlist2ranklist(df.loc[index].values)
            df.loc[index]=np.array(result,dtype=np.int16)
        print(df)
        newpath=os.path.join('corr_20_rank',name)
        df.to_excel(newpath)
def main():
    name_list=['上证指数.xlsx', '中小板指.xlsx', '创业板指.xlsx', '区块链.xlsx', '医药制造.xlsx', '工业互联网.xlsx', '数字货币.xlsx', '深证成指.xlsx', '白酒.xlsx', '芯片.xlsx', '蚂蚁金服.xlsx']
    
    # name_list=['白酒.xlsx']
    for name in name_list:
        res=rank_stastic(name)
        newpath=os.path.join('my_rank',name)
        print(newpath)
        res.to_excel(newpath)
        
if __name__ == "__main__":
    # run1()
    main()