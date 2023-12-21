import pandas as pd
import re
from collections import defaultdict
from tqdm import tqdm

'''
__init__(self, series)
    這個方法初始化BPE物件。它接受一個pandas Series（通常是文本數據集的一部分），
    並創建一個詞彙表，    其中的鍵是數據集中的不同單詞，值是每個單詞的出現次數。
    單詞之間的字符用空格分隔。

_get_stats(self, vocab)
    這個私有方法計算詞彙表中每對相鄰字符的頻率。
    這是通過使用defaultdict來存儲字符對和其頻率計數來完成的。

merge_vocab(self, pair, v_in)
    這個方法合併詞彙表中指定的字符對。
    它接受一個字符對和當前詞彙表作為輸入，然後返回一個新的詞彙表，其中該字符對已合併。

run(self, num_merges)
    這個方法是BPE算法的主要部分。它執行指定次數的合併操作。

首先，它使用_get_stats方法獲取當前詞彙表中的字符對統計信息。
然後，它找到頻率最高的字符對，並使用merge_vocab方法對其進行合併。
它將結果存儲在vocab_res和best_res列表中，這些列表用於保存合併的結果和最佳配對。
最終，run方法返回這些列表，其中包括每一步合併的結果
'''
class BytepairEncoding:
    def __init__(self, series):
        self.vocab = {}
        for val in tqdm(series.value_counts().reset_index().values):
            k = ' '.join(val[0])+' ' 
            self.vocab[k] = val[1]

    def _get_stats(self, vocab):
        '''
        給定一個詞彙表（將單詞映射到頻率計數的字典），返回一個字典，
        表示詞彙表中字符對的頻率計數的元組。
        '''
        
        pairs = defaultdict(int)
        for word, freq in vocab.items():
            symbols = word.split()
            for i in range(len(symbols) - 1):
                pairs[symbols[i], symbols[i + 1]] += freq
        return pairs
    def merge_vocab(self, pair, v_in):
        """
        給定一對字符和一個詞彙表，返回一個新的詞彙表，
        其中將這對字符在詞彙表中出現的地方合併在一起。
        同時更新這對字符在新詞彙表中的頻率計數。
        """
        v_out = {}
        bigram = re.escape(' '.join(pair))
        # r'(?<!\S)' => 前面沒有空白
        p = re.compile(r'(?<!\S)' + bigram + r'(?!\S)')
        for word in v_in:
            #p.sub(''.join(pair), word)是在word中查找所有匹配p的字符對，
            #並使用''.join(pair)替換它們
            w_out = p.sub(''.join(pair), word)
            v_out[w_out] = v_in[word]
        return v_out
    
    def run(self, num_merges:int):
        '''
        --------params--------
        num_merges: 合併操作的次數，type: int
        --------return--------
        best_res: 每次合併的最佳字符對，type: list
        '''    
        # 用於存儲合併後的詞彙表
        vocab_res = [] 
        # 用於存儲每個迭代中合併的最佳字符對
        best_res = [] 
        # 迭代進行指定次數的合併
        for i in tqdm(range(num_merges)): 
            # 獲取當前詞彙表中的字符對統計
            pairs = self._get_stats(self.vocab)
            if len(pairs) == 0:break
            # 找到出現最頻繁的字符對
            best = max(pairs, key=pairs.get)
            # 將最佳字符對存儲到 best_res
            best_res.append(best)              
            print(f'best pair: {best}')
            # 將最佳字符對合併到當前詞彙表
            self.vocab = self.merge_vocab(best, self.vocab) 
            # 檢查字符對的最大長度是否為 2
            if len(max(best, key=len)) == 2:   
                print(f'new vocab: {self.vocab}')
                # 將合併後的字符添加到 vocab_res
                vocab_res.extend([x for x in best if len(x) >= 2]) 
            # 檢查字符對的最大長度是否為 3
            if len(max(best, key=len)) == 3:   
                print(f'add in list: {best}')
                # 將合併後的字符添加到 vocab_res
                vocab_res.append(best[0] + best[1])
            print('-' * 30)
        self.vocab_res = set(vocab_res) 
        return best_res 
text =['壽司郎', '壽司郎三重', '壽司郎新莊', '壽司郎(12/21期)', '藏壽司', '德州太平'
       , '德州']

bpe2= BytepairEncoding(pd.Series(text))
bpe2.run(200)
bpe2.vocab_res