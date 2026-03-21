import torch.nn as nn

class UltraPower(nn.Module):
    def __init__(self, in_feature, out_feature):
        
        super(UltraPower, self).__init__()

        self.l1 = nn.Linear(in_feature, 16) # 1x4 @ 4 x 16 = 1x16
        self.l2 = nn.Linear(16, 16) # 1x16 @ 16x16 = 1x16
        self.l3 = nn.Linear(16, 4) # 1x16 @ 16x4 = 1x4
        self.relu1 = nn.ReLU()
        self.l4 = nn.Linear(4, out_feature) # 1x4 @ 4xout

    def forward(self, x):
        # x = 1x4
        x = self.l1(x) # 1x16
        x = self.l2(x)
        x = self.l3(x)
        x = self.relu1(x)
        x = self.l4(x)
        return x