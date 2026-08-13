from model import *

flag = "firebird{mayb3_n3xt_tim3_r3ver5e_LLM_1nstead}"
tokenized_flag = tokenizer(flag)

biases = [0, 0, 0]
biases[0] = torch.tensor([0.0, 0.0], dtype=torch.float32)
biases[1] = torch.tensor([0.0] * 196, dtype=torch.float32)
biases[2] = torch.tensor([-4 * 49 * 100.0 + 50], dtype=torch.float32)

weights = [0, 0, 0]
weights[0] = torch.tensor([[[1.0, 1.0]], [[2.0, 3.0]]], dtype=torch.float32)
weights[1] = torch.zeros(
    (4 * 49, 2 * 49),
    dtype=torch.float32,
)
weights[2] = torch.full(
    (1, 4 * 49),
    100.0,
    dtype=torch.float32,
)
results = []
for i in range(49):
    results.append(tokenized_flag[0][i] + tokenized_flag[0][i + 1])
for i in range(49):
    results.append(2 * tokenized_flag[0][i] + 3 * tokenized_flag[0][i + 1])
for i in range(2 * 49):
    weights[1][2 * i][i] = 100
    weights[1][2 * i + 1][i] = -100
    biases[1][2 * i] = -results[i] * 100 + 50
    biases[1][2 * i + 1] = results[i] * 100 + 50

model = FlagChecker()
model.conv1d.weight.data = weights[0]
model.conv1d.bias.data = biases[0]

model.fc1.weight.data = weights[1]
model.fc1.bias.data = biases[1]

model.fc2.weight.data = weights[2]
model.fc2.bias.data = biases[2]

# Save the model
torch.save(model.state_dict(), "model.pth")
