import pandas as pd
import os
from MyModel import MyModel

import torch
import torch.nn as nn
import torch.optim as optim

from tqdm import tqdm

print(f"Path: {os.getcwd()}")

data_path = "./data_analytics/data/SSMA_preprocessed.csv"

df = pd.read_csv(data_path)
df = df.iloc[:, 2:]

df['Addicted_Score'] = df['Addicted_Score'].astype('category').cat.codes
num_classes = df["Addicted_Score"].nunique()

d = 0.8

train_data = df[0:int(len(df)*d)]
X_train = train_data.drop("Addicted_Score", axis=1)
y_train = train_data["Addicted_Score"]

test_data = df[int(len(df)*d):len(df)]
X_test = test_data.drop("Addicted_Score", axis=1)
y_test = test_data["Addicted_Score"]

X_train = torch.tensor(X_train.values.astype(float), dtype=torch.float32)
y_train = torch.tensor(y_train.values.astype(float), dtype=torch.long)

X_test = torch.tensor(X_test.values.astype(float), dtype=torch.float32)
y_test = torch.tensor(y_test.values.astype(float), dtype=torch.long)


model = MyModel(X_train.shape[1], num_classes)

optimizer = optim.SGD(model.parameters(), lr=1e-3)
criterion = nn.CrossEntropyLoss()

epochs = 5000
loss_history = []

for epoch in tqdm(range(epochs)):
    optimizer.zero_grad()

    pred = model(X_train)
    loss = criterion(pred, y_train)
    loss_history.append(loss.item())
    loss.backward()

    optimizer.step()

    if epoch % 100 == 0:
        print(f"epoch: {epoch}, loss: {loss}")


print(f"Total loss: {loss}")

model.eval()
with torch.no_grad():
    pred = model(X_test)

    _, predicted_classes = torch.max(pred, dim=1)

    correct = (predicted_classes == y_test).sum().item()
    acc = (correct / len(y_test)) * 100

    print(f"acc : {acc:.2f}")

data = X_test[:5]
print(data)

print(model(data))
prob = torch.softmax(model(data), dim=1)

print(prob)

print(torch.argmax(prob, dim=1).tolist())

print(y_test[:5])


# 실제로 내 데이터로 예측해보기
my_data = [24.0000,  0.0000,  1.0000,  7.7000, 0.0000 ,6.5000,  8.0000,  0.0000, 0.0000,  1.0000,  0.0000]
my_data_tensor = torch.tensor(my_data, dtype=torch.float32).unsqueeze(0)

print(model(my_data_tensor))
prob = torch.softmax(model(my_data_tensor), dim=1)

print(prob)

print(torch.argmax(prob, dim=1).item())

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report

plt.figure(figsize=(10, 5))
plt.plot(loss_history, label='Training Loss')
plt.title('Training Loss Over Epochs')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)
plt.show()

# 2. 테스트 데이터 예측값 얻기
model.eval()
with torch.no_grad():
    outputs = model(X_test)
    _, preds = torch.max(outputs, 1)

# Tensor를 Numpy 배열로 변환 (시각화 라이브러리용)
y_true = y_test.cpu().numpy()
y_pred = preds.cpu().numpy()

# 3. 혼동 행렬 (Confusion Matrix) 시각화
cm = confusion_matrix(y_true, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=range(num_classes), 
            yticklabels=range(num_classes))
plt.title('Confusion Matrix')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()

# 4. 상세 지표 출력 (Precision, Recall, F1-score)
print("\n[Classification Report]")
print(classification_report(y_true, y_pred))