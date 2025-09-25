import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier 
from sklearn.model_selection import train_test_split 
from sklearn.metrics import classification_report 
from micromlgen import port  # 转换成c代码
import pickle


# 0. 先做个函数提取特征
def extract_features(df):
    return [
            df['yaw'].mean(), df['yaw'].std(), df['yaw'].max(), df['yaw'].min(),
            df['pitch'].mean(), df['pitch'].std(), df['pitch'].max(), df['pitch'].min(),
            df['roll'].mean(), df['roll'].std(), df['roll'].max(), df['roll'].min(),]

# 1. 尝试加载所有的CSV文件.
def load_data(folder):
    X, y = [], []
    label = os.path.basename(folder)
    for file in os.listdir(folder):
        if file.endswith('.csv'):
            df = pd.read_csv(os.path.join(folder, file))
            # 提取时域特征 
            features = extract_features(df)
            X.append(features)
            y.append(label)
    return X, y 


# 2. 加载所有类别 
X_all, y_all = [], []

for gesture in ['circle', 'cross', 'left', 'right']:
    X, y = load_data(f'data/{gesture}')
    X_all.extend(X)
    y_all.extend(y)

X_all = np.array(X_all)
print(f"X_all.shape = {X_all.shape}")

# 3. 训练模型
X_train, X_test, y_train, y_test = train_test_split(X_all, y_all, test_size=0.2) 
clf = RandomForestClassifier(n_estimators=30, max_depth=10)
clf.fit(X_train, y_train)

with open("my_esp32-gesture-RFmodel.pkl", 'wb') as f:
    pickle.dump(clf, f)

# 4. 评估模型
print(classification_report(y_test, clf.predict(X_test)))
print('-'* 50)
print(f"训练集准确率: {clf.score(X_all, y_all):.2f}")

# 5. 导出一个C头文件，后面烧录到esp32

with open('model.h', 'w') as f:
    f.write(port(clf))

print(f"已经生成model.h头文件")



