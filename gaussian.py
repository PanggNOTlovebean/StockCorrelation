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
import math
from matplotlib.pyplot import MultipleLocator,tick_params
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
    result["pctChg"] = result.apply(lambda x: float(x['pctChg']), axis=1)
    result["Date"] = result.apply(
        lambda x: datetime.datetime.strptime(x['Date'], "%Y-%m-%d"), axis=1)
    result.set_index('Date', inplace=True)
    # 登出系统
    bs.logout()
    return result
def code2name(code):
    rs=pd.read_csv('./code_name.csv',encoding='gbk')
    rs.set_index('code',inplace=True)
    return rs.loc[code]['code_name']

def main2():
    index_list=['上证指数','中小板指','创业板指','深证成指']
    code_list=['sh.000001','sz.399005','sz.399006','sz.399106']
    start_date='2019-09-01'
    end_date='2020-11-01'
    
    for i in range(4):
        name=index_list[i]
        boss=get_stock_data(code=code_list[i],start_date=start_date,end_date=end_date)
        print(boss)
        # boss=boss['2020']
        path = os.path.join('板块个股代码',name+'.txt')
        with open(path) as fp:
            result=pd.DataFrame(columns=['date'])
            result['date']=boss.index
            content=fp.readlines()
            for line in content:
                try:
                    rs=get_stock_data(code=line[:-1],start_date=start_date,end_date=end_date)
                    x=np.array(rs['pctChg'].values)
                    base=np.array(boss['pctChg'].values)
                    new_x=x-base
                    rs['pctChg']=new_x
                    stock_name=code2name(line[:-1])
                    result[stock_name]=new_x
                except:
                    continue
            result=result.set_index('date')
            res_path=os.path.join('股票相对涨跌幅2',name+'.csv')
            result.to_csv(res_path)
        i=i+1     
    return
def main():
    name_list=['区块链', '医药制造', '工业互联网', '数字货币', '白酒', '芯片', '蚂蚁金服']
    # name_list=['芯片', '蚂蚁金服']
    # index_list=['上证指数','中小板指','创业板指','深证成指']
    # name_list=['白酒']
    
    start_date='2019-09-01'
    end_date='2020-11-01'
    
    for name in name_list:
        mypath=os.path.join('板块指数2',name+'.csv')
        boss=pd.read_csv(mypath,encoding='utf-8',engine='python')
        boss["date"] = boss.apply(
        lambda x: datetime.datetime.strptime(x['date'], "%Y-%m-%d"), axis=1)
        boss.set_index('date',inplace=True)
        # boss=boss['2020']
        path = os.path.join('板块个股代码',name+'.txt')
        with open(path) as fp:
            result=pd.DataFrame(columns=['date'])
            result['date']=boss.index
            content=fp.readlines()
            for line in content:
                try:
                    rs=get_stock_data(code=line[:-1],start_date=start_date,end_date=end_date)
                    x=np.array(rs['pctChg'].values)
                    base=np.array(boss['pctChg'].values)*100
                    new_x=x-base
                    rs['pctChg']=new_x
                    stock_name=code2name(line[:-1])
                    result[stock_name]=new_x
                except:
                    continue
            result=result.set_index('date')
            res_path=os.path.join('股票相对涨跌幅2',name+'.csv')
            result.to_csv(res_path)       
    return
def relative_20():
    name_list=['区块链', '医药制造', '工业互联网', '数字货币', '白酒', '芯片', '蚂蚁金服','上证指数','中小板指','创业板指','深证成指']
    # name_list=['白酒']
    for name in name_list:
        path=os.path.join('股票相对涨跌幅',name+'.csv')
        df=pd.read_csv(path,engine='python',encoding='utf-8')
        df['date']=df.apply(lambda x:datetime.datetime.strptime(x['date'],'%Y-%m-%d'),axis=1)
        df.set_index('date',inplace=True)
        result=pd.DataFrame(columns=['date'])
        result['date']=df.index
        result.set_index('date',inplace=True)
        for column in df.columns:
                up_down=[]
                for i in range(len(df[column])):
                    if(i<19):
                        up_down.append(np.nan)
                        i=i+1
                        continue
                    up_down.append(np.sum(df[column][i-19:i+1]))
                    i=i+1
                result[column]=up_down
        newpath=os.path.join('股票20日相对涨跌幅',name+'.csv')
        result.to_csv(newpath,encoding='utf-8')

def gaussian(sigma, x, u):
	y = np.exp(-(x - u) ** 2 / (2 * sigma ** 2)) / (  math.sqrt(2 * math.pi))
	return y

def paint():
    industry='白酒'
    name='山西汾酒'
    path=os.path.join('股票20日相对涨跌幅',industry+'.csv')
    df=pd.read_csv(path,engine='python',encoding='utf-8')
    df['date']=df.apply(lambda x:datetime.datetime.strptime(x['date'],'%Y-%m-%d'),axis=1)
    df=df.set_index('date')
    y=df['2020'][name]
    print(y)
    fig=plt.figure()
    fig.canvas.set_window_title(industry+'-'+name)
    # ax=plt.histogram(y,bins=25,histtype="stepfilled",normed=True,alpha=0.6)

    sns.set()
    # 
    ax=sns.distplot(y,bins=50,kde_kws={"color": "r", "lw": 1, "label": "KDE",'bw_adjust':.4},)

    # ax=sns.distplot(y,bins=50,kde=False,norm_hist=False)
    # ax = sns.kdeplot(y,
    #              color='r',
    #              cumulative=True,bw_adjust=.4)
    
    # ax.legend()
    ax.set_xlabel('Change')
    ax.set_ylabel('Probability')
    path=os.path.join('概率分布',industry+'-'+name+'.png')
    plt.savefig(path)
    plt.show()

def get_my_score(y):
    kd=KernelDensity(bandwidth=.4)
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
    # industry='白酒'
    # name='五粮液'
    # path=os.path.join('股票20日相对涨跌幅',industry+'.csv')
    # df=pd.read_csv(path,engine='python',encoding='utf-8')
    # df['date']=df.apply(lambda x:datetime.datetime.strptime(x['date'],'%Y-%m-%d'),axis=1)
    # df=df.set_index('date')
    # y=df['2020'][name].values
    name_list=['白酒','区块链', '医药制造', '工业互联网', '数字货币',  '芯片', '蚂蚁金服','上证指数','中小板指','创业板指','深证成指']
    for name in name_list:
        path=os.path.join('股票20日相对涨跌幅',name+'.csv')
        df=pd.read_csv(path,engine='python',encoding='utf-8')
        df['date']=df.apply(lambda x:datetime.datetime.strptime(x['date'],'%Y-%m-%d'),axis=1)
        df=df.set_index('date')
        result=pd.DataFrame(columns=['name','prob'])
        for column in df.columns:
            y=df['2020'][column].values
            the_score=get_my_score(y)
            result=result.append({'name':column,'prob':the_score[0]},ignore_index=True)
        print(result)
        path=os.path.join('my_prob',name+'.csv')
        result.to_csv(path)
    # kd=KernelDensity(bandwidth=.4)
    # kd=kd.fit(y.values.reshape(-1,1))
    # z=kd.score_samples(y.values.reshape(-1,1))
    # # # plt.figure()
    # # # plt.scatter(y,np.exp(z))
    # # print(z)
    # # plt.show()
    # min=np.min(y.values)
    # array_x=np.linspace(start=min,stop=y.values[-1],num=1000)
    # sum=0
    # print(y.values[-1])
    # for i in (range(1,len(array_x))):
    #     dx=array_x[i]-array_x[i-1]
    #     sum=sum+dx*np.exp(kd.score_samples(array_x[i].reshape(-1,1)))
    # print(sum)      
    return
def merge_csv():
    name_list=['白酒','区块链', '医药制造', '工业互联网', '数字货币',  '芯片', '蚂蚁金服','上证指数','中小板指','创业板指','深证成指']
    for name in name_list:
        path1=os.path.join('my_rank',name+'.xlsx')
        path2=os.path.join('my_prob',name+'.csv')
        df1=pd.read_excel(path1)
        df2=pd.read_csv(path2,engine='python',encoding='utf-8')
        result=pd.merge(left=df1,right=df2,on='name')
        result=result.drop('Unnamed: 0',axis=1)
        result['prob_flag']=result['prob']>0.4
        result['prob_sigma']=0.4
        print(result)
        path3=os.path.join('my_way',name+'.csv')
        result.to_csv(path3)

def run2():
    name_list=['白酒','区块链', '医药制造', '工业互联网', '数字货币',  '芯片', '蚂蚁金服','上证指数','中小板指','创业板指','深证成指']
    for name in name_list:
        path1=os.path.join('my_way',name+'.csv')
        df1=pd.read_csv(path1,engine='python',encoding='utf-8')
        df2=df1[(df1['prob_flag']) & (df1['rank']<50)].get(['name','score','prob'])
        score_value=df2['score'].values
        print(score_value)
        min=np.min(score_value)
        max=np.max(score_value)
        new_score=(score_value-min)/(max-min)
        df2['new_score']=new_score
        df2['sum']=0.3*df2['prob']+0.7*df2['new_score']
        print(df2)
if __name__ == '__main__':
    # main2()

    # main()
    # relative_20()
    paint()
    # density()
    # merge_csv()
    # run2()
    # x = np.linspace(-4, 8, 10000)
    # plt.plot(x,gaussian(1,x,1),color='#570200',linewidth=.99)
    # plt.plot(x,gaussian(1,x,2),color='#570200',linewidth=.99)
    # plt.plot(x,gaussian(1,x,3),color='#570200',linewidth=.99)
    # x=np.ones(50)
    # y=np.linspace(0,np.max(gaussian(1,x,1)),50)
    # print(x)
    # plt.plot(x, y, color = '#570200', linewidth=.99, linestyle="--")
    # x=np.ones(50)*2
    # plt.plot(x, y, color = '#570200', linewidth=.99, linestyle="--")
    # x=np.ones(50)*3
    # ax=plt.plot(x, y, color = '#570200', linewidth=.99, linestyle="--")
    # ax=plt.gca()
    # x_major_locator=MultipleLocator(1)
    # ax.xaxis.set_major_locator(x_major_locator)
    # ax.tick_params(length=0)
    # plt.plot()
    # plt.show()
    # x = np.linspace(-8, 8, 10000)

    # plt.plot(x,gaussian(1,x,0),linewidth=.99,label='h=1')
    # plt.plot(x,gaussian(0.2,x,0),linewidth=.99,label='h=0.2')
    # plt.plot(x,gaussian(5,x,0),linewidth=.99,label='h=5')




    
    # y=gaussian(1,x,1)+gaussian(1,x,2)+gaussian(1,x,3)+gaussian(1,x,7)+gaussian(1,x,8)+gaussian(1,x,9)
    # y=y/6
    # plt.plot(x, y, color='#00008B', linewidth=.99)

    # ax=plt.gca()
    # x_major_locator=MultipleLocator(2)
    # ax.xaxis.set_major_locator(x_major_locator)
    # ax.tick_params(length=0)
    # plt.legend()
    # plt.plot()
    # plt.show()