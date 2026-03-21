import torch
import torch.optim as optim

import os
import matplotlib.pyplot as plt

from HyperParam import HyperParam as hp
from tqdm import tqdm

# Load your model here, named as 'model'
# from {file_name} import {model name} as RegressionModel

# example
from models.UltarPower import UltraPower as RegressionModel

def train(model, x_train, y_train, epochs=hp.epochs):
    model_name = model.__class__.__name__

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
                save_fn = f"{model_name}_best.pth"
                torch.save(model.state_dict(), os.path.join(hp.save_path, save_fn))
                best_loss = loss

            # 시각화
            ax.cla()
            ax.scatter(x_train.numpy(), y_train.numpy(), color='blue', label='Real Data', s=100)
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
    print("\n--- Starting Challenges ---")
    model = RegressionModel(1, 1)
    x_hard, y_hard = generate_data(n_samples=1000)
    train(model, x_hard, y_hard)