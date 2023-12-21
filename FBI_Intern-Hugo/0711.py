import pandas as pd
import re

# 测试示例数据
name=[
    '連加*德州(10/11期)',
    '德州 14,300(01/06期)',
    '連加*德州(10/11期)'
]
id=[1,2,1]
df=pd.DataFrame({'name':name,'id':id})
df['id'].value_counts()
df['count']=df.groupby('id')['name'].transform('count')
df=df.loc[df[df['id']]['name'].str.contains('連加*').all()==False]
for i in id:
    if df[df['id']==i]['name'].str.contains('連加*').all():
        continue
    a=df[df['id']==i].value_counts()
df[df['id']==1]['name'].str.contains('連加*')      

 
def extract_text(text, pattern):
    match = re.search(pattern, text)
    if match:
        text = match.group(1)
    return text
strings=[
    '112年使用牌照稅 33333333333333',
    '112年使用牌照稅33333333333333',
    '112年燃料稅33333333333333',
    '連加*免稅店2222'
]
pattern = r'\d+年([\u4e00-\u9fff]+稅)'

for string in strings:
    result = extract_text(string, pattern)
    print(f"{string} > {result}")

