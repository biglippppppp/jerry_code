import tensorflow as tf
from transformers import BertTokenizer, TFBertForSequenceClassification

# 範例數據
texts = ["這是一條正面文本", "這是一條負面文本"]
labels = [1, 0]

# 加載分詞器和模型
model_name = 'bert-base-chinese'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = TFBertForSequenceClassification.from_pretrained(model_name, num_labels=2)

# 分詞和準備數據集
# Tokenize and prepare the dataset
inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="tf")
dataset = tf.data.Dataset.from_tensor_slices(((inputs['input_ids'], inputs['attention_mask'], inputs['token_type_ids']), labels)).shuffle(len(texts))

#dataset = tf.data.Dataset.from_tensor_slices((dict(inputs), labels)).shuffle(len(texts))

# 定義優化器和損失函數
optimizer = tf.keras.optimizers.Adam(learning_rate=2e-5)
loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

# 編譯模型
model.compile(optimizer=optimizer, loss=loss, metrics=['accuracy'])

# 微調
batch_size = 2
epochs = 3
model.fit(dataset.batch(batch_size), epochs=epochs)

# 使用微調後的模型進行預測
new_text = "這是一個待分類的文本"
new_input = tokenizer(new_text, return_tensors="tf")
predictions = model.predict(new_input)
predicted_label = tf.argmax(predictions.logits, axis=1).numpy()[0]

label_mapping = {0: "負面", 1: "正面"}
print("預測標籤:", label_mapping[predicted_label])
