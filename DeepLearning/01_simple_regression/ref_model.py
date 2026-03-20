import torch
import torch.nn as nn

class SimpleModel(nn.Module):
    def __init__(self, in_feature, out_feature):
        super(SimpleModel, self).__init__()

        self.l1 = nn.Linear(in_feature, 16) # 1x16
        self.relu1 = nn.ReLU() 
        self.l2 = nn.Linear(16, 16) # 1x16 @ 16x16 = 1x16
        self.relu2 = nn.ReLU()
        self.l3 = nn.Linear(16, 4) # 1x16 @ 16x4 = 1x4
        self.relu3 = nn.ReLU()
        self.l4 = nn.Linear(4, out_feature)

    def forward(self, x):
        x = self.l1(x)
        x = self.relu1(x)

        x = self.l2(x)
        x = self.relu2(x)

        x = self.l3(x)
        x = self.relu3(x)
        
        x = self.l4(x)
        return x

class LinearModel(nn.Module):
    def __init__(self, in_feature, out_feature):
        super(LinearModel, self).__init__()

        self.l1 = nn.Linear(in_feature, 16) # 1x4 @ 4 x 16 = 1x16
        self.l2 = nn.Linear(16, 16) # 1x16 @ 16x16 = 1x16
        self.l3 = nn.Linear(16, 4) # 1x16 @ 16x4 = 1x4
        self.l4 = nn.Linear(4, out_feature) # 1x4 @ 4xout

    def forward(self, x):
        # x = 1x4
        x = self.l1(x) # 1x16
        x = self.l2(x)
        x = self.l3(x)
        x = self.l4(x)
        return x

class ComplexModel(nn.Module):
    def __init__(self, in_feature, out_feature):
        super(ComplexModel, self).__init__()

        self.model = nn.Sequential(
            nn.Linear(in_feature, 128),
            nn.ReLU(),
            
            nn.Linear(128, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),

            nn.Linear(64, out_feature)
        )

    def forward(self, x):
        return self.model(x)