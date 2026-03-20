import torch
import torch.optim as optim

import os
import matplotlib.pyplot as plt

from HyperParam import HyperParam as hp
from tqdm import tqdm

from ref_model import ComplexModel as RegressionModel

# Simple dataset
# y = 3x + 2
x_train = torch.FloatTensor([[1], [2], [3], [4], [5]])
y_train = torch.FloatTensor([[5], [8], [11], [14], [17]])

# model은 데이터만 가지고 판단합니다.
# 즉, 3x + 2 라는걸 모르고 있습니다!
# 학습을 반복하면서, 모델은 데이터가 가리키는 함수가 3x + 2라는 것을 알게 될 겁니다

def train(model, x_train, y_train, epochs=hp.epochs):
    if not os.path.exists(hp.save_path):
        os.makedirs(hp.save_path)

    plt.ion()
    fig, ax = plt.subplots(figsize=(8, 5))

    optimizer = optim.Adam(model.parameters(), lr=hp.lr)

    pbar = tqdm(range(epochs), desc="Training... ")

    best_loss = 1

    for epoch in pbar:
        optimizer.zero_grad()

        pred = model(x_train)
        
        # MSELoss 사용
        loss = torch.mean((pred- y_train) ** 2)

        loss.backward()
        optimizer.step()

        if (epoch + 1) % 100 == 0:
            pbar.set_postfix(loss=f"{loss.item():.6f}")
            if loss < best_loss:
                best_loss = loss

            # 시각화
            ax.cla()
            ax.scatter(x_train.numpy(), y_train.numpy(), color='blue', label='Real Data', s=20)
            ax.plot(x_train.numpy(), pred.detach().numpy(), color='red', lw=3, label='Model Prediction')
            ax.set_title(f'Training Epoch: {epoch}', fontsize=15)
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.legend()
            ax.grid(True, linestyle='--')
            plt.pause(0.1)

    plt.ioff()
    print(f"Done! mse: {loss}, best: {best_loss}")
    plt.show()

def generate_data(n_samples=1000):
        # x 범위를 -3에서 3 사이로 설정
        x = torch.linspace(-3, 3, n_samples).view(-1, 1)
        
        # 복합 함수: sin(5x) + 0.5*cos(10x) + 0.1*x^2
        # 1. 고주파 진동 (sin, cos)
        # 2. 비대칭성 (x^2)
        y = torch.sin(5 * x) + 0.5 * torch.cos(10 * x) + (0.1 * x**2)
        noise = torch.randn(x.size()) * 0.05
        y += noise
        
        return x, y

if __name__ == "__main__":
    '''
    # Level 1: 직선 학습
    print("--- Starting Level 1: Linear Regression ---")
    model = RegressionModel(1, 1)
    train(model, x_train, y_train, 10000)

    test_inputs = torch.FloatTensor([[0.0], [5.0]])
    model.eval()
    with torch.no_grad():
         pred = model(test_inputs)
    
    # 정말로 y = 3x + 2를 예측했을까?
    y0 = pred[0].item()   # x=0 일 때의 y값 (즉, 절편 b)
    y10 = pred[1].item()  # x=10 일 때의 y값

    # 기울기(a) 계산: (y2 - y1) / (x2 - x1)
    slope = (y10 - y0) / (5.0 - 0.0)
    bias = y0

    print(f"최종 산출식: y = {slope:.4f}x + {bias:.4f}")
    '''

    # Level 2: 곡선 학습 (Challenge)
    print("\n--- Starting Level 2: Challenges ---")
    model = RegressionModel(1, 1)
    x_hard, y_hard = generate_data(n_samples=1000)
    train(model, x_hard, y_hard, 100000)