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
df = df.iloc[:,2:]

d = 0.8

train_data = df[0:int(len(df)*d)]
X_train = train_data.drop("Affects_Academic_Performance", axis=1)
y_train = train_data["Affects_Academic_Performance"]

test_data = df[int(len(df)*d):len(df)]
X_test = test_data.drop("Affects_Academic_Performance", axis=1)
y_test = test_data["Affects_Academic_Performance"]

X_train = torch.tensor(X_train.values.astype(float), dtype=torch.float32)
y_train = torch.tensor(y_train.values.astype(float), dtype=torch.float32).view(-1, 1)

X_test = torch.tensor(X_test.values.astype(float), dtype=torch.float32)
y_test = torch.tensor(y_test.values.astype(float), dtype=torch.float32).view(-1, 1)

model = MyModel(train_data.shape[1] - 1, 1)

optimizer = optim.SGD(model.parameters(), lr=1e-3)
criterion = nn.BCELoss()

epochs = 5000
sig = lambda x: 1/(1+torch.exp(-x))

for epoch in tqdm(range(epochs)):
    optimizer.zero_grad()

    pred = model(X_train)
    
    pred_sig = sig(pred)
    loss = criterion(pred_sig, y_train)

    loss.backward()

    optimizer.step()

    if epoch % 100 == 0:
        print(f"epoch: {epoch}, loss: {loss}")


print(f"Total loss: {loss}")

model.eval()
with torch.no_grad():
    pred = model(X_test)

    prediction_binary = (pred >= 0.5).float()

    correct = (y_test == prediction_binary).sum().item()
    acc = (correct / len(y_test)) * 100

    print(f"acc : {acc:.2f}")

data = X_test[:5]
print(data)

print(sig(model(data)))

print(sig(model(data)) >= 0.5)

print(y_test[:5])


# 실제로 내 데이터로 예측해보기
my_data = [24.0000,  0.0000,  1.0000,  7.7000,  6.5000,  8.0000,  0.0000,  7.0000, 0.0000,  1.0000,  0.0000]
my_data = torch.Tensor(my_data)

print(sig(model(my_data)))

print(sig(model(my_data)) >= 0.5)