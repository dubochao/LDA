import pandas as pd
import time
path = "./data/article.csv"
df=pd.read_csv(path,encoding="utf_8_sig")
# df= df.drop_duplicates(subset=['text'],keep='first')#删除重复数据
time_complete = df['time']
support_count=df['support_count']
for index,i in enumerate(time_complete):
    try:
        df['time'][index]= time.strftime('%Y/%m/%d',time.strptime(i, '%Y-%m-%d'))
    except:
        pass
for index,i in enumerate(support_count):
    try:
        df['support_count'][index]=int(df['support_count'][index])
    except:
        pass
df= df.drop_duplicates(subset=['text'],keep='first')#删除重复数据
df.to_csv(path,encoding="utf_8_sig",header=True,index=False)
# df.to_csv(path,encoding="utf_8_sig",header=True,index=False)
