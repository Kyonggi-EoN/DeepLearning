import torch.nn as nn

class Miracle(nn.Module):
    def __init__(self, in_feature, out_feature):
        
        super(Miracle, self).__init__()
        
        # 각각의 Linear에 ReLU 활성화 함수를 붙여줘서 더 복잡한 모델을 만듦.
        self.l1 = nn.Linear(in_feature, 16) # 1x4 @ 4 x 16 = 1x16
        self.relu1 = nn.ReLU() 
        self.l2 = nn.Linear(16, 64) # 1x16 @ 16 x 64 = 1x64
        self.relu2 = nn.ReLU()
        self.l3 = nn.Linear(64, 128) # 1x64 @ 64x128 = 1x128
        self.relu3 = nn.ReLU()
        self.l4 = nn.Linear(128, 256) # 1x128 @ 128x256 = 1x256
        self.relu4 = nn.ReLU()
        self.l5 = nn.Linear(256, out_feature) # 1x256 @ 256x1 = 1x1

    def forward(self, x):
        # x = 1x4
        x = self.l1(x) # 1x16
        x = self.relu1(x)
        x = self.l2(x)
        x = self.relu2(x)
        x = self.l3(x)
        x = self.relu3(x)
        x = self.l4(x)
        x = self.relu4(x)
        x = self.l5(x)
        return x