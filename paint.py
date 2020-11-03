import pandas as pd
import os
def main():
    BASE_DIR = os.path.abspath(os.curdir)
    path = os.path.join(BASE_DIR,'corr_20_all_result')
    result=[]
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path,file))==True:
            dt=pd.read_excel(os.path.join(path,file))
            a={}
            for index,row in dt.iterrows():
                if(int(row['avg_rank'])<4):
                    a[row['avg_rank']]=index
            for i in [1,2,3]:
                print('{名称:\''+dt.iloc[a[i]]['name']+'\''+',相关性均值:'+str(round(dt.iloc[a[i]]['corr_avg'],3))+',所属指数:\''+file.split('.')[0]+'\'},')
if __name__ == "__main__":
    main()