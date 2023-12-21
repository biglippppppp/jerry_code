import re
from collections import defaultdict
from tqdm import tqdm
#https://huggingface.co/learn/nlp-course/chapter6/5?fw=pt
#https://www.geeksforgeeks.org/byte-pair-encoding-bpe-in-nlp/
'''
這段程式碼包含了幾個主要函數：
get_vocab(data): 
    get_vocab 函數用於建立詞彙表，它接受一個字符串列表 data 作為輸入，並返回一個字典，
    該字典將單詞映射到它們在 data 中出現的頻率計數。它將每個單詞按字元拆分，
    並在單詞結尾添加 </w> 作為結束標記，然後將單詞添加到詞彙表中。

get_stats(vocab): 
    get_stats 函數用於獲取詞彙表中字符對的頻率計數。
    它接受詞彙表字典 vocab 作為輸入，然後遍歷詞彙表中的每個單詞。
    對於每個單詞，它將單詞按空格拆分成符號（characters），並遍歷這些符號的組合，
    計算字符對的頻率計數。這樣得到的 pairs 字典將表示詞彙表中字符對的頻率計數。

byte_pair_encoding(data, n): 
    byte_pair_encoding 函數是主要的 BPE 編碼函數。
    它接受字符串列表 data 和整數 n 作為輸入，並返回一個由 n 個字符對組成的列表。
    它使用 get_vocab 函數建立詞彙表，然後在 n 次迭代中，使用 get_stats 函數獲取字符對的頻率計數，
    並使用 merge_vocab 函數進行字符合併，然後更新詞彙表。最終，它返回合併後的字符對列表。

merge_vocab(pair, v_in): 
    merge_vocab 函數用於合併詞彙表中字符對。
    它接受一對字符 pair 和詞彙表 v_in 作為輸入，然後使用正則表達式來尋找在詞彙表中出現的這個字符對，
    並將它們合併成新的字符。合併後的字符添加到新的詞彙表 v_out 中，並返回該詞彙表。
 '''
def get_vocab(data):
    """
    給定一個字符串列表，返回一個單詞映射到其在數據中頻率計數的字典。
    """
    
    vocab = defaultdict(int)
    for line in data:
        for word in line.split():
            vocab[' '.join(list(word)) + ' </w>'] += 1
    return vocab


def get_stats(vocab):
    '''
    給定一個詞彙表（將單詞映射到頻率計數的字典），返回一個字典，
    表示詞彙表中字符對的頻率計數的元組。
    '''
    pairs = defaultdict(int)
    for word, freq in vocab.items():
        symbols = word.split()
        for i in range(len(symbols) - 1):
            pairs[symbols[i], symbols[i + 1]] += freq

    
    #確保在返回pairs字典之前，確保它至少包含一個字符對。
    # if not pairs:
    #     return {(' ', '</w>'): 1}

    return pairs


# def merge_vocab(pair, v_in):
#     """
#     給定一對字符和一個詞彙表，返回一個新的詞彙表，
#     其中將這對字符在詞彙表中出現的地方合併在一起。
#     """
#     v_out = {}
#     #re.escape() 是 Python 中 re 模塊（正則表達式）提供的一個函數，用於對字串中的特殊字符進行轉義，
#     #讓這些特殊字符在正則表達式中作為普通字符進行匹配。
#     #ex:re.escape('www.python.org') = 'www\\.python\\.org'
#     bigram = re.escape(' '.join(pair))
#     p = re.compile(r'(?<!\S)' + bigram + r'(?!\S)')
#     for word in v_in:
#         w_out = p.sub(''.join(pair) , word) 
#         #w_out = p.sub(''.join(pair), word)
#         v_out[w_out] = v_in[word]
#     return v_out

def merge_vocab(pair, v_in):
    """
    給定一對字符和一個詞彙表，返回一個新的詞彙表，
    其中將這對字符在詞彙表中出現的地方合併在一起。
    同時更新這對字符在新詞彙表中的頻率計數。
    """
    v_out = {}
    #re.escape() 是 Python 中 re 模塊（正則表達式）提供的一個函數，用於對字串中的特殊字符進行轉義，
    #讓這些特殊字符在正則表達式中作為普通字符進行匹配。
    #ex:re.escape('www.python.org') = 'www\\.python\\.org'
    bigram = re.escape(' '.join(pair))
    #?!<\S 的意思是「後面不可以跟隨 < 符號後接一個非空白字符」
    p = re.compile(r'(?<!\S)' + bigram + r'(?!\S)')
    for word in v_in:
        w_out = p.sub(''.join(pair), word)
        v_out[w_out] = v_in[word]
    return v_out


def byte_pair_encoding(data, n):
    """
    給定一個字符串列表和一個整數 n，返回一個由 n 個在輸入數據的詞彙表中找到的字符對組成的列表。
    """
    vocab = get_vocab(data)
    for i in range(n):
        pairs = get_stats(vocab)
        if len(pairs) == 0:
            break
        best = max(pairs, key=pairs.get)
        vocab = merge_vocab(best, vocab)
    return vocab

# 例子：
corpus = ''' 
石二鍋。
石二鍋是一家餐廳。
石二鍋三重。
石二鍋三重店。
石二鍋三重店的鍋很好吃。
石二鍋-三重店。
石二鍋-三重店的鍋很好吃。
石二鍋(期)。

'''
data = corpus.split('。')

n = 200
bpe_pairs = byte_pair_encoding(data, n)
bpe_pairs



# # Example usage:
# corpus = '''Tokenization is the process of breaking down 
# a sequence of text into smaller units called tokens,
# which can be words, phrases, or even individual characters.
# Tokenization is often the first step in natural languages processing tasks 
# such as text classification, named entity recognition, and sentiment analysis.
# The resulting tokens are typically used as input to further processing steps,
# such as vectorization, where the tokens are converted
# into numerical representations for machine learning models to use.'''
# data = corpus.split('.')
  
# n = 230
# bpe_pairs = byte_pair_encoding(data, n)
# bpe_pairs





