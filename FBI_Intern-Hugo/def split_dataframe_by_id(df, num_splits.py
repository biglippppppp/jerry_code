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
    'id': [1, 1, 2, 2, 3, 4, 5, 31,32, 4, 4, 5, 5, 5,5,5, 6, 6,
           1, 1, 2, 2, 3, 4, 5, 31,32, 4, 4, 5, 5, 5,5,5, 6, 6,
           1, 1, 2, 2, 3, 4, 51, 31,32, 4, 4, 5, 5, 5,5,5, 6, 6,
           1, 1, 2, 2, 3, 4, 51, 31,32, 4, 4, 5, 5, 5,5,5, 6, 6,
           1, 1, 2, 2, 3, 4, 51, 31,32, 4, 4, 5, 5, 5,5,5, 6, 6
           ],
    'value': [10, 20, 30, 40, 44,44, 40, 50, 60, 70,4,4, 70, 80, 90, 100, 110, 120,
              10, 20, 30, 40, 44,44, 40, 50, 60, 70,4,4, 70, 80, 90, 100, 110, 120,
              10, 20, 30, 40, 44,44, 40, 50, 60, 70,4,4, 70, 80, 90, 100, 110, 120,
              10, 20, 30, 40, 44,44, 40, 50, 60, 70,4,4, 70, 80, 90, 100, 110, 120,
              10, 20, 30, 40, 44,44, 40, 50, 60, 70,4,4, 70, 80, 90, 100, 110, 120
              ]
}

df = pd.DataFrame(data)

# 設定切分成幾份
num_splits = 50
split_dfs_optimized = split_dataframe_by_id_optimized(df, num_splits)

split_dfs_optimized


# 將DataFrame切分成指定的份數
split_dfs = split_dataframe_by_id(df, num_splits)

# 顯示切分後的結果
for i, split_df in enumerate(split_dfs):
    print(f"DataFrame {i + 1}:")
    print(split_df)
    print()


import pandas as pd
import numpy as np
import math

def split_dataframe_by_id_optimized(df:pd.DataFrame, num_splits:int):
    '''
    input:
        df: 要切分的DataFrame
        num_splits: 要切分成幾份
    output:
        split_dfs: 切分後的DataFrame列表，每個元素都是一個DataFrame，type: list
    '''
    # 按照ID進行排序
    df_sorted = df.sort_values(by='id')
    
    # 使用groupby函數按照ID分組
    grouped = list(df_sorted.groupby('id'))

    # 計算每一份的行數（平均分配）
    total_rows = len(df)
    split_rows = math.ceil(total_rows / num_splits)

    split_dfs = []
    current_rows = 0
    current_grouped = []

    for _, group in grouped:
        num_rows = len(group)
        if current_rows + num_rows <= split_rows or len(split_dfs) == num_splits - 1:
            current_grouped.append(group)
            current_rows += num_rows
        else:
            split_dfs.append(pd.concat(current_grouped))
            current_grouped = [group]
            current_rows = num_rows

    split_dfs.append(pd.concat(current_grouped))

    return [df.reset_index(drop=True) for df in split_dfs]

# 假設有一個DataFrame df，其中包含'id'欄位用於識別不同的ID
data = {
    'id': [1, 1, 2, 2, 3, 4, 5, 3, 3, 4, 4,4.5, 5, 5, 5, 5, 5, 6, 6,7],
    'value': [10, 20, 30, 40, 44, 44, 40, 50,44, 60, 70, 4, 4, 70,88, 80, 90, 100, 110, 120]
}

df = pd.DataFrame(data)

# 設定切分成幾份
num_splits = 3

# 將DataFrame切分成指定的份數
split_dfs_optimized = split_dataframe_by_id_optimized(df, num_splits)

split_dfs_optimized
