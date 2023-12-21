exclude_list.sort(key=len, reverse=True)
df['already'] = 0

for i in range(len(exclude_list)):
    print(exclude_list[i])
    df["value"] = df.apply(lambda row: exclude_list[i] if exclude_list[i] in row["value"] else row["value"], axis=1)
    df["already"] = df.apply(lambda row: 1 if exclude_list[i] in row["value"] else row["already"], axis=1)

df