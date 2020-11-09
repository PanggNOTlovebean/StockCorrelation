import os
import pandas as pd
import json
import os
from numpy.lib.shape_base import column_stack
import pandas as pd 
import numpy as np
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties
import json
import baostock as bs
from sklearn.neighbors import KernelDensity
from sklearn.cluster import KMeans

def numlist2ranklist(nums):
    args=np.argsort(1-np.array(nums,dtype=np.float32))

    result=np.zeros(len(args),dtype=np.int16)
    i=1
    for num in args:
        result[num]=i
        i=i+1
    return result

def main():
    name_list=['白酒','区块链', '医药制造', '工业互联网', '数字货币',  '芯片', '蚂蚁金服','上证指数','中小板指','创业板指','深证成指']
    for name in name_list:
        path1=os.path.join('my_prob',name+'.csv')
        path2=os.path.join('my_prob2',name+'.csv')
        df1=pd.read_csv(path1,engine='python',encoding='utf-8')
        df2=pd.read_csv(path2,engine='python',encoding='utf-8')
        # prob_x是收益率得分 prob_y是相关性得分
        df3=pd.merge(df1,df2,on='name').get(['name','prob_x','prob_y'])
        df3['score']=1.2-np.sqrt((1-df3['prob_x'])*(1-df3['prob_x'])+(1-df3['prob_y'])*(1-df3['prob_y']))
        df3['ret_score']=df3['prob_x']
        df3['corr_score']=df3['prob_y']
        ranks=numlist2ranklist(df3['score'].values)
        df3['rank']=ranks
        df3=df3.get(['name','corr_score','ret_score','score','rank'])
        path3=os.path.join('end',name+'.csv')
        df3.to_csv(path3)
    return
def main2():
    name='医药制造'
    path=os.path.join('end',name+'.csv')
    df=pd.read_csv(path,engine='python',encoding='utf-8')
    x=df['corr_score'].values
    y=df['ret_score'].values
    plt.figure()
    z=np.vstack((x,y)).T

    ax=plt.scatter(x,y,c=((1-x)*(1-y))*((1-x)*(1-y)),marker='.')
    plt.colorbar()
    plt.xlabel('corr')
    plt.ylabel('ret')
    plt.show()


    # n_cluster=3
    # y_pred=KMeans(n_clusters=4,random_state=9).fit_predict(z)
    # print(y_pred)
    # plt.scatter(z[:,0],z[:,1],c=y_pred,marker='+')
    # plt.show()
if __name__ == '__main__':
    # main2()
    main()