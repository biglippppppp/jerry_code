import re
import pandas as pd

text = ['德州 14,300(01/06期)','連家*德州(10/11期)', 'play st(10/11期)']
text2=['麻州 14,300(01/06期)', '德州(10/11期)','連家*德州(10/11期)', 'play st(10/11期)']

data2=pd.DataFrame(text2,columns=['text'])
data2['id']=[i for i in range(len(text2))]
data = pd.DataFrame(text, columns=['text'])
data['id'] = [i for i in range(len(text))]
data2.merge(data, on='id', how='left')
merged_data = data2.merge(data, on='id', how='left')
merged_data['text_y'] = merged_data['text_y'].fillna(merged_data['text_x'])
merged_data = merged_data.drop(columns='text_x').rename(columns={'text_x': 'text'})
merged_data.id = [0,0,2,2]
split = len(merged_data) // 2
for i in range(split):
    if merged_data['id'][i] == merged_data['id'][i+1]:
        i+=1
    print(i)
    data = merged_data[:i+1]
    print(data)
    
print(merged_data)


# 使用正则表达式提取中文和英文部分，并将结果存储在名为 'text2' 的新列中
data['text2'] = data['text'].str.extract(r'(^[a-zA-Z\s\u4e00-\u9fff\*]+)')
data['text3']=data['text'].apply(lambda x: x.str.extract(r'(^[a-zA-Z\s\u4e00-\u9fff\*]+)')if '期'in x else x)
data
payment=['連家']
for p in payment:
    data['text2'] = data['text2'].str.replace(r'[\*' + p + ']', '')

print(data)

import pandas as pd

strings = [
    "playstation 01 32,22",
    "富邦 01 333,22(01/02期)",
    "富邦人壽 2 + 6632,22(01/30期)",
    "連家*家樂福 632,22(01/30期)",
    "連家*網購-9 6632,22(01/30期)",
    "playstation 01 32,22(01/02期)",
    "蝦皮-9 play 6632,22(01/30期)"
    "playstation 01 32,22",
    "富邦 01 333,22(01/02期)",
    "富邦人壽 2 + 6632,22(01/30期)",
    "連家*家樂福 632,22(01/30期)",
    "連家*網購-9 6632,22(01/30期)",
    "playstation 01 32,22(01/02期)",
    "蝦皮-9 play 6632,22(01/30期)"
]

data = pd.DataFrame(strings, columns=['text'])
data['id'] = [0, 1, 1, 1, 2, 3, 4,1, 1, 1, 2, 3, 4]
df = pd.DataFrame(data['id'].unique(),columns=['id'])
df['count'] = data['id'].value_counts()
# 平均分組
average_group_size = df['count'].sum() //2
df['group'] = (df['count'].cumsum() - average_group_size) // average_group_size + 1
df['group'] = df['group'].astype(int)

# 合併結果
result = data.merge(df[['id', 'group']], on='id')
result


# 测试示例数据
strings = [
    "playstation 01 32,22",
    "富邦 01 333,22(01/02期)",
    "富邦人壽 2 + 6632,22(01/30期)",
    "連家*家樂福 632,22(01/30期)",
    "連家*網購-9 6632,22(01/30期)",
    "playstation 01 32,22(01/02期)",
    "蝦皮-9 play 6632,22(01/30期)"
]

data=pd.DataFrame(strings,columns=['text'])
data['id'] = [0,1,1,1,2,3,4]
split = len(data) // 2

for i in range(split):
    k=0
    while data['id'][i+k] == data['id'][i+k+1]:
        k+=1
    print(k)
    data1 = data[split*i:split*(i+1)+k]
    print(data1)
# 测试示例数据
strings = [
    "playstation 01 32,22",
    "富邦 01 333,22(01/02期)",
    "富邦人壽 2 + 6632,22(01/30期)",
    "連家*家樂福 632,22(01/30期)",
    "連家*網購-9 6632,22(01/30期)",
    "playstation 01 32,22(01/02期)",
    "蝦皮-9 play 6632,22(01/30期)"
]

data=pd.DataFrame(strings,columns=['text'])

def repay(series,pattern):
    series = series.astype(str).apply(lambda x:
        re.findall(pattern, x)[0].strip() 
        if re.match(pattern, x) else x)
    return series
def delete_str(series,key_word_list):
    for key_word in key_word_list:
        series=series.apply(lambda x: x if key_word not in x else x.replace(key_word,''))
    return series
data['text2']=repay(data['text'],r'^(.+?)\s+\d+.*\(\d+/\d+期\)$')
strings = [
    "playstation 01 32,22",
    "富邦 01 333,22(01/02期)",
    "富邦人壽 2 + 6632,22(01/30期)",
    "連家*家樂福 632,22(01/30期)",
    "連家*網購-9 6632,22(01/30期)",
    "playstation 01 32,22(01/02期)",
    "蝦皮-9 play 6632,22(01/30期)",
    "pi-支付連-家樂福 632,22(01/30期)"
]

data=pd.DataFrame(strings,columns=['text'])
df=data
import re
import numpy as np
payment=[r'連家*','蝦皮-9','pi-']
def delete_str(df, key_word_list):
    df['text3'] = df['text2'].apply(lambda x: next((kw for kw in payment if kw in x), None))
    df['text3'] = df['text3'].str.replace(r'\W+', '')
    for key_word in payment:
        print(key_word)
        df['text2'] = df['text2'].str.replace(key_word, '', regex=False)
    
   
    return df


data=delete_str(data,payment)
data

string=['北市停車費xxxx',
        '北市停車費退回xxx']
re.findall(r'w+停車費(?!退回)',string[0])


separator = "#"
combined_string = separator.join(strings)

substring_count = {}

for i in range(len(combined_string)):
    for j in range(i+1, len(combined_string)):
        substring = combined_string[i:j]
        if substring in substring_count:
            substring_count[substring] += 1
        else:
            substring_count[substring] = 1

max_count = max(substring_count.values())
longest_substrings = [substring for substring, count in substring_count.items() if count == max_count]

print("最长重复子字符串：", longest_substrings)







import pandas as pd

# 假設有一個DataFrame df，其中包含'id'欄位用於識別不同的ID，並且想要將其平均切分成兩份
# 這裡假設ID欄位是一個整數或字符串，以便進行排序。

# 創建一個範例DataFrame
data = {
    'id': [1, 1, 2, 2, 3, 3, 4, 4, 5, 5],
    'value': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
}

df = pd.DataFrame(data)

# 按照ID進行排序
df = df.sort_values(by='id')
# 使用groupby函數按照ID分組
grouped = df.groupby('id')
# 計算DataFrame的行數
total_rows = len(df)
# 計算每一份的行數（平均分配），注意這裡要用grouped.size()來獲得每個ID的行數
split_rows = total_rows // 2
# 初始化兩個DataFrame
df1 = pd.DataFrame(columns=df.columns)
df2 = pd.DataFrame(columns=df.columns)

# 依次將每個ID的行數分配到兩個DataFrame中
for _, group in grouped:
    if len(df1) < split_rows:
        df1 = pd.concat([df1, group])
    else:
        df2 = pd.concat([df2, group])

# 重置索引
df1 = df1.reset_index(drop=True)
df2 = df2.reset_index(drop=True)

# 顯示結果
print("DataFrame 1:")
print(df1)
print("\nDataFrame 2:")
print(df2)



import pandas as pd
import math

def split_dataframe_by_id(df, num_splits):
    '''
    input:
        df: 要切分的DataFrame
        num_splits: 要切分成幾份
         
    '''
    # 按照ID進行排序
    df = df.sort_values(by='id')
    # 使用groupby函數按照ID分組
    grouped = df.groupby('id')
    # 計算每一份的行數（平均分配），注意這裡要用grouped.size()來獲得每個ID的行數
    id_counts = grouped.size()
    total_rows = len(df)
    #向上取整數
    split_rows = math.ceil(total_rows / num_splits)
    # 初始化多個DataFrame，存儲切分後的結果
    split_dfs = [pd.DataFrame(columns=df.columns) for _ in range(num_splits)]

    current_split = 0
    current_rows = 0

    # 依次將每個ID的行數分配到多個DataFrame中
    # 其中id_value是分組的ID值，group是包含該ID值相關行的DataFrame。
    for id_value, group in grouped:
        num_rows = len(group)
        if current_rows + num_rows <= split_rows:
            split_dfs[current_split] = pd.concat([split_dfs[current_split], group])
            current_rows += num_rows
        else:
            # 如果當前DataFrame已滿，則換到下一個DataFrame
            while current_rows + num_rows > split_rows:
                current_split += 1
                current_rows = len(split_dfs[current_split])
            split_dfs[current_split] = pd.concat([split_dfs[current_split], group])
            current_rows += num_rows

    # 重置索引並返回所有切分後的DataFrame
    return [df.reset_index(drop=True) for df in split_dfs]

# 假設有一個DataFrame df，其中包含'id'欄位用於識別不同的ID
data = {
    'id': [1, 1, 2, 2, 3,4, 5,3, 4, 4, 5, 5, 5, 6, 6],
    'value': [10, 20, 30,40, 44,40, 50, 60, 70, 70, 80, 90, 100, 110, 120]
}

df = pd.DataFrame(data)

# 設定切分成幾份
num_splits = 3

# 將DataFrame切分成指定的份數
split_dfs = split_dataframe_by_id(df, num_splits)

# 顯示切分後的結果
for i, split_df in enumerate(split_dfs):
    print(f"DataFrame {i + 1}:")
    print(split_df)
    print()


import pandas as pd
import math

def split_dataframe_by_id(df, num_splits):
    # 按照ID進行排序
    df = df.sort_values(by='id')

    # 使用groupby函數按照ID分組
    grouped = df.groupby('id')

    # 計算每一份的行數（平均分配），注意這裡要用grouped.size()來獲得每個ID的行數
    id_counts = grouped.size()
    total_rows = len(df)
    split_rows = math.ceil(total_rows / num_splits)

    # 初始化多個DataFrame，存儲切分後的結果
    split_dfs = [pd.DataFrame(columns=df.columns) for _ in range(num_splits)]

    current_split = 0
    current_rows = 0

    # 依次將每個ID的行數分配到多個DataFrame中
    for id_value, group in grouped:
        num_rows = len(group)
        if current_rows + num_rows <= split_rows or current_split == num_splits - 1:
            # 如果當前DataFrame還可以容納該ID的行數，或者是最後一個DataFrame，則放入當前DataFrame
            split_dfs[current_split] = pd.concat([split_dfs[current_split], group])
            current_rows += num_rows
        else:
            # 否則換到下一個DataFrame
            current_split += 1
            split_dfs[current_split] = pd.concat([split_dfs[current_split], group])
            current_rows = num_rows

    # 重置索引並返回所有切分後的DataFrame
    return [df.reset_index(drop=True) for df in split_dfs]

# 假設有一個DataFrame df，其中包含'id'欄位用於識別不同的ID
data = {
    'id': [1, 1, 2, 2, 3, 4, 5, 3,3, 4, 4, 5, 5, 5,5,5, 6, 6],
    'value': [10, 20, 30, 40, 44,44, 40, 50, 60, 70,4,4, 70, 80, 90, 100, 110, 120]
}

df = pd.DataFrame(data)

# 設定切分成幾份
num_splits = 3

# 將DataFrame切分成指定的份數
split_dfs = split_dataframe_by_id(df, num_splits)

# 顯示切分後的結果
for i, split_df in enumerate(split_dfs):
    print(f"DataFrame {i + 1}:")
    print(split_df)
    print()
df[~df['id'].isin([1,2,3,4,5,6])]