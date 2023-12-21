def find_longest_common_substring(a, b):
    m = len(a)
    n = len(b)
    # 创建一个二维数组用于记录子问题的解
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    # 记录最长公共子字符串的长度和结束位置
    max_length = 0
    end_pos = 0
    # 动态规划的过程
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > max_length:
                    max_length = dp[i][j]
                    end_pos = i
    # 提取最长公共子字符串
    longest_substring = a[end_pos - max_length:end_pos]
    return longest_substring
def find_longest_common_substr(df,id_column,id,target_column,merge_round):
    list = df[df[id_column]==id][target_column].to_list()
    if len(list) == 1:
        return list[0]
    else:
        tmp_str = find_longest_common_substring(list[0], list[1])
        round_count = 0
        for i in range(len(list)-2):
            tmp_str_a = find_longest_common_substring(tmp_str, list[i+2])
            if tmp_str_a == tmp_str:
                round_count+=1
            else:
                round_count = 0
            tmp_str = tmp_str_a
            if round_count > merge_round:
                return tmp_str
        return tmp_str