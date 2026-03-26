import torch.nn as nn

class jo23mk(nn.Module):
    def __init__(self, in_feature, out_feature):
        super(jo23mk, self).__init__()

        self.l1 = nn.Linear(in_feature, 16) 
        self.relu1 = nn.ReLU()
        self.l2 = nn.Linear(16, 16)
        self.relu2 = nn.ReLU()

        self.l21 = nn.Linear(16, 32)
        self.relu21 = nn.ReLU()

        self.l3 = nn.Linear(32, 16)
        self.relu3 = nn.ReLU()
        self.l4 = nn.Linear(16, out_feature)

    def forward(self, x):
        x = self.l1(x)
        x = self.relu1(x)

        x = self.l2(x)
        x = self.relu2(x)

        x = self.l21(x)
        x = self.relu21(x)

        x = self.l3(x)
        x = self.relu3(x)
        
        x = self.l4(x)
        return x