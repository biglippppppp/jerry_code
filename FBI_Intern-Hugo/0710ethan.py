import re
import collections
from operator import itemgetter

from collections import defaultdict

class longest_substring:
    def __init__(self, strings):
        self.strings = strings

    def get_stats(self, vocab):
        #collections.defaultdict(int) 來創建一個預設值為0的字典 pairs
        pairs = collections.defaultdict(int)
        for word, freq in vocab.items():
            #word.split() 的目的是將 word 字符串按照默認的分隔符（空格）進行分割
            symbols = word.split()
            for i in range(len(symbols)-1):
                pairs[symbols[i], symbols[i+1]] += freq
        return pairs

    def merge_vocab(self, pair, v_in):
        v_out = {}
        bigram = re.escape(' '.join(pair))
        p = re.compile(r'(?<!\S)' + bigram + r'(?!\S)')
        for word in v_in:
            #使用正則表達式模式 p 將 word 中與詞對匹配的部分替換為合併後的詞。
            # ''.join(pair) 將詞對中的詞彙連接成一個字符串，作為替換的內容
            w_out = p.sub(''.join(pair), word)
            v_out[w_out] = v_in[word]
        return v_out

    def create_vocab(self, strings):
        #collections.defaultdict(int) 來創建一個預設值為0的字典 vocab
        vocab = defaultdict(int)
        for string in strings:
            string = ' '.join(string)
            vocab[string] += 1
        vocab_dict = dict(vocab)
        return vocab_dict

    def main(self, num_merges=10):
        vocab = self.create_vocab(self.strings)
        history_res = defaultdict(int)
        for i in range(num_merges):
            pairs = self.get_stats(vocab)
            best = max(pairs, key=pairs.get)
            vocab = self.merge_vocab(best, vocab)
            history_res[best[0]] += 1
        history_res = sorted(history_res.items(), key=itemgetter(1), reverse=True)
        return history_res[0][0], history_res[0][1]

strings = ['石二鍋家樂福重新', '石二鍋捷運後山埤', '石二鍋士林中正',
           '石二鍋高雄華夏']
longest_substring(strings).main()
        
def get_stats(vocab):
    #collections.defaultdict(int) 來創建一個預設值為0的字典 pairs
    pairs = collections.defaultdict(int)
    for word, freq in vocab.items():
        # 將詞拆分為符號（字符）序列
        symbols = word.split()
        for i in range(len(symbols)-1):
            pairs[symbols[i],symbols[i+1]] += freq
    return pairs

def merge_vocab(pair, v_in):
    v_out = {}
    bigram = re.escape(' '.join(pair))
    p = re.compile(r'(?<!\S)' + bigram + r'(?!\S)')
    for word in v_in:
        #使用正則表達式模式 p 將 word 中與詞對匹配的部分替換為合併後的詞。
        # ''.join(pair) 將詞對中的詞彙連接成一個字符串，作為替換的內容
        w_out = p.sub(''.join(pair), word)
        v_out[w_out] = v_in[word]
    return v_out

strings = ['新北市停車費', '高雄停車費', '台南停車費',
           '北市停車費']

def create_vocab(strings):
    vocab = defaultdict(int)
    # 遍历每个字符串，将每个字符作为词汇表的一个词，并计数出现次数
    for string in strings:
        string = ' '.join(string)
        vocab[string] += 1
    # 将词汇表转换为字典形式
    vocab_dict = dict(vocab)
    return vocab_dict

vocab = create_vocab(strings)

num_merges = 15
#建立有default值的字典，default值为int()，即0
history_res = defaultdict(int)
for i in range(num_merges):
    pairs = get_stats(vocab)
    best = max(pairs, key=pairs.get)
    vocab = merge_vocab(best, vocab)
    history_res[best[0]] += 1
    

history_res = sorted(history_res.items(), key=itemgetter(1), reverse=True)
history_res[0][0]

#%%
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
longest_substrings = [substring for substring in longest_substrings if len(substring) > 1]
longest_substrings = sorted(longest_substrings, key=len, reverse=True)
print("最常重複字串：", longest_substrings[0], "，出現次數：", max_count)

# %%
from collections import defaultdict

def find_most_frequent_substring(df, col1,col2):
    substring_count = defaultdict(int)
    max_count = 1
    longest_substrings = []

    for string in strings:
        n = len(string)
        for i in range(n):
            for j in range(i+1, n+1):
                substring = string[i:j]
                print(substring)
                substring_count[substring] += 1
                count = substring_count[substring]
                if count > max_count and len(substring) > 1:
                    max_count = count
                    longest_substrings = [substring]
                elif count == max_count and substring not in longest_substrings:
                    longest_substrings.append(substring)
    longest_substrings = sorted(longest_substrings, key=len, reverse=True)
    
    return longest_substrings, max_count
substring_count = defaultdict(int)
max_count = 1
longest_substrings = []
strings = ['play station00000', 'play st000', 'play station00000']
for string in strings:
    string=re.sub(r'\d+', '', string)
    print(string)
    n = len(string)
    for i in range(n):
        for j in range(i+1, n+1):
            substring = string[i:j]
            substring_count[substring] += 1
            count = substring_count[substring]
            if count > max_count and len(substring) > 1:
                max_count = count
                longest_substrings = [substring]
            elif count == max_count and substring not in longest_substrings:
                longest_substrings.append(substring)
longest_substrings = sorted(longest_substrings, key=len, reverse=True)
print(longest_substrings[0], "出現次數：", max_count)
longest_substrings, max_count = find_most_frequent_substring(strings)
longest_substrings = sorted(longest_substrings, key=len, reverse=True)
print("最常重複字串：", longest_substrings[0], "，出現次數：", max_count)


import re

# pattern = r'^(.+?)\s+\d+.*\(\d+/\d+期\)'
# pattern = r'([A-Za-z|\u4e00-\u9fff|\*\-|0-9]+) (.+)\(\d+/\d+期\)'
#pattern = r'([A-Za-z|\u4e00-\u9fff|\*]+)([\*\-|0-9]+)? (.+)\(\d+/\d+期\)'

pattern = r'([A-Za-z|\u4e00-\u9fff|\*\s]+)([\*\-|0-9]+\s)?(.+)\(\d+/\d+期\)'

def extract_text(text, pattern):
    match = re.search(pattern, text)
    if match:
        text = match.group(1)
    return text

# 测试示例数据
strings = [
    "playstation 01 * 32,22",
    "元大人壽111 333,22(01/02期)",
    "富邦人壽10* 6632,22(01/30期)",
    "德周太平店 143,00(01/36期)",
    "連家*家樂福 6632,22(01/30期)",
    "連家*網購-9 6632,22(01/30期)",
    "play station 01 32,22(01/02期)",
    "net太平店 143,00(01/36期)",
     "元大人壽 (01/02期)",
    "富邦人壽10* (01/30期)",
    "play station (01/02期)",
    "ssss(01/36期)"
]

for string in strings:
    result = extract_text(string,pattern)
    print(f"{string} > {result}")
    
pattern2 = r'([A-Za-z|\u4e00-\u9fff|\*\s]+)(\s)?\(\d+/\d+期\)'
   
strings2 = [
    "元大人壽 (01/02期)",
    "富邦人壽10* (01/30期)",
    "play station (01/02期)",
    "ssss(01/36期)"
    
]
for string in strings2:
    result = extract_text(string,pattern2)
    print(f"{string} > {result}")
    


# %%
