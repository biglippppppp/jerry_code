def fill_english(df):
    """
    解決問題：中文格子為空值時，將英文格子填入並只取英文部分
    input:原始資料，type:dataframe
    """
    df_new = df[df['tag'].isnull()]
    df_new['tag'] = df_new['merchant_edesc_lower'].str.extract(r"([a-zA-Z]+)")
    """
    output:更新後資料 type:dataframe
    """
    return merging(df, df_new)