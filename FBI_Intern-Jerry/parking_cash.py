
def parking_cash(df):
    """
    解決停車場費格式問題
    intput:原始資料 type:dataframe
    """
    df_new = df[df['tag'].str.contains('停車費')]
    df_new['tag'] = df_new['tag'].str.extract(r"([\u4e00-\u9fff]+)")
    """
    output:更新後資料 type:dataframe
    """
    return merging(df, df_new)