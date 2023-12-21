def category_in_english(df,pattern_column,target_column,word_list):
    """
    功能：當英文店名中含有特定pattern時取代tag為該pattern
    input: 
            df:原資料，資料格式：dataframe
            pattern_column:欲尋找之英文column，資料格式：str
            target_column:目標column 資料格式：str
            word_list:欲尋找英文pattern 資料格式：list
    output:修改後df 資料格式：dataframe
    """
    for key in word_list:
        df[target_column] = df[target_column].where(~df[pattern_column].str.contains(key), key)
    return df