
#%%

from transformers import BertTokenizer, TFBertForSequenceClassification
from sklearn.model_selection import train_test_split
import tensorflow as tf
# 你的文本和標籤樣本
texts = ["石二鍋相信，日子不該日復一日，試著嘗試一些新鮮事，就能讓生活充滿新鮮感，讓自己活力滿滿。讓品嚐新鮮成為一件簡單的事情，石二鍋嚴選新鮮食材及新鮮口味"
         , "必勝客股份有限公司是美國著名的披薩連鎖餐廳。截至2018年12月31日，必勝客在全球擁有18,431家餐廳，是世界上最大的披薩連鎖店。它是百勝餐飲集團的子公司。 丹·卡尼和法蘭克·卡尼兩兄弟在1958年憑母親借來的600美元於美國堪薩斯州威奇托創立首間必勝客，第二年在同州首府托彼卡市建立首間特許經營的必勝客。"
         , "各式戶外運動專業裝備專賣，多元的品牌、豐富的款式、實在的價格，超殺的優惠，運動愛好者必逛！ 商品橫跨跑步、訓練、戶外等，從休閒到專業，給你最齊全的運動裝備與體驗，快來逛逛！"]
labels = [['餐廳','火鍋店'], ['餐廳','pizza'], ['運動用品']] 

# 1. 建立標籤到索引的映射，並從索引到標籤的映射

# all_labels：包含所有唯一標籤的集合。
# label2idx：一個字典，用於查找每個標籤的索引。
#           {'火鍋店': 0, 'pizza': 1, '運動用品': 2, '餐廳': 3}
# idx2label：一個字典，用於查找每個索引的標籤
#           {0: '火鍋店', 1: 'pizza', 2: '運動用品', 3: '餐廳'}
#建立標籤集合
all_labels = set([label for sublist in labels for label in sublist])
#從標籤到索引的映射
label2idx = {label: idx for idx, label in enumerate(all_labels)}
#從索引到標籤的映射:
idx2label = {idx: label for label, idx in label2idx.items()}

# 2. 轉換字符串標籤為二進制編碼
def encode_labels(labels):
    encoded = []
    for label_list in labels:
        # 這裡，我們為當前的標籤列表創建了一個全為0的列表。
        # 其長度等於所有可能的標籤的總數。
        encoded_labels = [0] * len(all_labels)
        for label in label_list:
            encoded_labels[label2idx[label]] = 1
        encoded.append(encoded_labels)
    return encoded

encoded_labels = encode_labels(labels)

# 將數據分割為訓練和測試集
train_texts, test_texts, train_labels, test_labels = train_test_split(
                                                    texts, 
                                                    encoded_labels, 
                                                    test_size=0.2)

# 定義分詞器和模型
tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")

# 3. 修改模型以適應正確的標籤數量
model = TFBertForSequenceClassification.from_pretrained("bert-base-chinese",
                                                        num_labels=len(all_labels))

# 定義損失函數和優化器
loss = tf.keras.losses.BinaryCrossentropy(from_logits=True)
optimizer = tf.keras.optimizers.Adam(learning_rate=2e-5)
model.compile(optimizer=optimizer, loss=loss)

# 對訓練和測試文本進行編碼
train_inputs = encode_texts(train_texts)
test_inputs = encode_texts(test_texts)

# 將標籤轉換為Tensor
train_labels = tf.convert_to_tensor(train_labels, dtype=tf.float32)
test_labels = tf.convert_to_tensor(test_labels, dtype=tf.float32)

# 訓練模型
model.fit(x=train_inputs, y=train_labels, epochs=3, batch_size=2)

# 進行預測
predictions = model.predict(test_inputs)
#這邊要調整
predicted_labels_bin = tf.sigmoid(predictions.logits) > 0.4

# 4. 預測後，將二進制的預測轉換回字符串標籤
def decode_predictions(predicted_labels_bin):
    decoded = []
    for pred in predicted_labels_bin:
        current_labels = []
        for idx, val in enumerate(pred):
            if val:
                current_labels.append(idx2label[idx])
        decoded.append(current_labels)
    return decoded

predicted_labels = decode_predictions(predicted_labels_bin.numpy())
print(test_labels,decode_predictions(test_labels.numpy()))
# 輸出預測結果
print(predicted_labels)
#%%
