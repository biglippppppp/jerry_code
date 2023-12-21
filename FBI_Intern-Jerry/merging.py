def merging(df, df_new):   
    df = df.merge(df_new, how="outer",on="id")
    df["tag_y"] = df["tag_y"].fillna(df["tag_x"])
    df = df.drop("tag_x",axis=1)
    df.rename(columns = {'tag_y':'tag'}, inplace = True) 
    return df