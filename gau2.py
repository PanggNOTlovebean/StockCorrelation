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
def paint():
    industry='白酒'
    name='青海春天'
    path=os.path.join('corr',industry+'.xlsx')
    df=pd.read_excel(path,sheet_name='20日相关性')
    df['date']=df.apply(lambda x:datetime.datetime.strptime(x['date'],'%Y-%m-%d'),axis=1)
    df=df.set_index('date')
    y=df['2020'][name]
    fig=plt.figure()
    fig.canvas.set_window_title(industry+'-'+name)
    # ax=sns.distplot(y,bins=50,kde_kws={"color": "r", "lw": 1, "label": "KDE",'bw_adjust':.2},)
    ax = sns.kdeplot(y,
                 color='r',
                 cumulative=True,bw_adjust=.2)
    ax.legend()
    ax.set_xlabel('Correction')
    ax.set_ylabel('Density')
    path=os.path.join('概率分布2',industry+'-'+name+'.png')
    plt.show()
def get_my_score(y):
    kd=KernelDensity(bandwidth=.2)
    kd=kd.fit(y.reshape(-1,1))
    z=kd.score_samples(y.reshape(-1,1))
    min=np.min(y)
    array_x=np.linspace(start=min,stop=y[-1],num=1000)
    sum=0
    for i in (range(1,len(array_x))):
        dx=array_x[i]-array_x[i-1]
        sum=sum+dx*np.exp(kd.score_samples(array_x[i].reshape(-1,1)))
    return sum  

def density():
    name_list=['白酒','区块链', '医药制造', '工业互联网', '数字货币',  '芯片', '蚂蚁金服','上证指数','中小板指','创业板指','深证成指']
    for name in name_list:
        path=os.path.join('corr',name+'.xlsx')
        df=pd.read_excel(path,sheet_name='20日相关性')
        df['date']=df.apply(lambda x:datetime.datetime.strptime(x['date'],'%Y-%m-%d'),axis=1)
        df=df.set_index('date')
        result=pd.DataFrame(columns=['name','prob'])
        
        for column in df.columns:
            y=df['2020'][column].values
            try:
                the_score=get_my_score(y)
            except:
                print(column)
                continue
            result=result.append({'name':column,'prob':the_score[0]},ignore_index=True)
        print(result)

        path=os.path.join('my_prob2',name+'.csv')
        result.to_csv(path)

def main():
    paint()
    # density()
    return

if __name__ == '__main__':
    main()