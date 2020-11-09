import os
import pandas as pd
import json
def main():
    name_list=['白酒','区块链', '医药制造', '工业互联网', '数字货币',  '芯片', '蚂蚁金服','上证指数','中小板指','创业板指','深证成指']
    result=pd.DataFrame(columns=['name','values','type','industry'])
    json_dict={}
    
    for name in name_list:
        path=os.path.join('corr_20_all_result',name+'.xlsx')
        df=pd.read_excel(path)
        json_list=[]
        for rank in [1,2,3,4,5]:
            for i in range(len(df)):
                if(df.iloc[i]['avg_rank']==rank):
                    json_list.append({'name':df.iloc[i]['name'],'value':float(format(df.iloc[i]['corr_avg'],'.4f')),'type':'均值','industry':name,'rank':str(df.iloc[i]['avg_rank']),})
                    json_list.append({'name':df.iloc[i]['name'],'value':float(format(df.iloc[i]['corr_range'],'.4f')),'type':'极差','industry':name,'rank':str(df.iloc[i]['avg_rank'])})
                    json_list.append({'name':df.iloc[i]['name'],'value':float(format(df.iloc[i]['corr_std'],'.4f')),'type':'标准差','industry':name,'rank':str(df.iloc[i]['avg_rank'])})
            json_dict[name]=json_list

    with open('./res1.json','w') as f:
        json.dump(json_dict,f,indent=4,ensure_ascii=False)

    # print(data)
    return
def main2():
    name_list=['白酒','区块链', '医药制造', '工业互联网', '数字货币',  '芯片', '蚂蚁金服','上证指数','中小板指','创业板指','深证成指']
    result=pd.DataFrame(columns=['name','values','type','industry'])
    json_dict={}
    
    for name in name_list:
        path=os.path.join('corr_20_all_result',name+'.xlsx')
        df=pd.read_excel(path)
        json_list=[]
        for rank in [1,2,3,4,5]:
            for i in range(len(df)):
                if(df.iloc[i]['avg_rank']==rank):
                    json_list.append({'name':df.iloc[i]['name'],'value':float(format(df.iloc[i]['corr_avg'],'.4f')),'type':'均值','industry':name,'rank':str(df.iloc[i]['avg_rank']),})
                    json_list.append({'name':df.iloc[i]['name'],'value':float(format(df.iloc[i]['corr_range'],'.4f')),'type':'极差','industry':name,'rank':str(df.iloc[i]['avg_rank'])})
                    json_list.append({'name':df.iloc[i]['name'],'value':float(format(df.iloc[i]['corr_std'],'.4f')),'type':'标准差','industry':name,'rank':str(df.iloc[i]['avg_rank'])})
            json_dict[name]=json_list

    with open('./res1.json','w') as f:
        json.dump(json_dict,f,indent=4,ensure_ascii=False)

    # print(data)
    return
def main2():
    name_list=['白酒','区块链', '医药制造', '工业互联网', '数字货币',  '芯片', '蚂蚁金服','上证指数','中小板指','创业板指','深证成指']
    result=pd.DataFrame(columns=['name','values','type','industry'])
    json_dict={}
    
    for name in name_list:
        path=os.path.join('my_way',name+'.csv')
        df=pd.read_csv(path,engine='python',encoding='utf-8')
        json_list=[]
        sum=0
        for rank in [1,2,4,5,6,7,8,9,10,11,12,13,14,15]:
            for i in range(len(df)):
                if(df.iloc[i]['rank']==rank and df.iloc[i]['prob_flag']==True):
                    sum=sum+1
                    json_list.append({'name':df.iloc[i]['name'],'value':float(format(df.iloc[i]['normal_score'],'.4f')),'type':'排名分','industry':name,'rank':str(df.iloc[i]['rank']),})
                    json_list.append({'name':df.iloc[i]['name'],'value':float(format(df.iloc[i]['prob'],'.4f')),'type':'状态分','industry':name,'rank':str(df.iloc[i]['rank'])})
            json_dict[name]=json_list
            if(sum==5):
                break
        print(json_dict)
            
    with open('./res2.json','w') as f:
        json.dump(json_dict,f,indent=4,ensure_ascii=False)
        
    # print(data)
    return
if __name__ == '__main__':
    # main()
    main2()