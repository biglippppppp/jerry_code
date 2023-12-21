def fill_91app(df):
    """
    解決問題：將格子內的[網購-9]改為[網購-91app]補齊
    input:原始資料，type:dataframe
    """
    df['tag'] = df['tag'].replace('網購-9', '網購-91app')
    """
    output:更新後資料 type:dataframe
    """
    return df