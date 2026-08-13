# This AI-based flag checker is powered by AI!
import torch

import torch.nn as nn
import torch.nn.functional as F


def tokenizer(input_string):
    ascii_values = [ord(char) for char in input_string]
    assert len(input_string) < 50, "Input string is too long"
    ascii_values += [0] * (50 - len(ascii_values))
    return torch.tensor([ascii_values], dtype=torch.float32)


class FlagChecker(nn.Module):
    def __init__(self):
        super(FlagChecker, self).__init__()
        self.conv1d = nn.Conv1d(
            in_channels=1,
            out_channels=2,
            kernel_size=2,
            stride=1,
        )
        self.fc1 = nn.Linear(2 * 49, 4 * 49)
        self.fc2 = nn.Linear(4 * 49, 1)

    def forward(self, x):
        x = x.unsqueeze(1)
        x = self.conv1d(x)
        x = x.view(x.size(0), -1)
        x = torch.sigmoid(self.fc1(x))
        x = torch.sigmoid(self.fc2(x))
        return x


if __name__ == "__main__":
    model = FlagChecker()
    model.load_state_dict(torch.load("model.pth"))
    model.eval()
    with torch.no_grad():
        input_tensor = tokenizer(input("Enter a flag: ").strip())
        output = model(input_tensor)
        if output.item() > 0.5:
            print("Correct flag")
        else:
            print("Incorrect flag")
