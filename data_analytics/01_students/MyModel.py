import torch.nn as nn

class MyModel(nn.Module):
    def __init__(self, in_feature, out_feature):
        super(MyModel, self).__init__()

        self.model = nn.Sequential(
            nn.Linear(in_feature, 128),
            nn.ReLU(),
            
            nn.Linear(128, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),

            nn.Linear(64, out_feature)
        )

    def forward(self, x):
        return self.model(x)