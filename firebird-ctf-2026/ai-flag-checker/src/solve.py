# %%
import torch

# %%
# Investigate the model weights
model_weights = torch.load("model.pth")
print(model_weights)

# %%

# Model architecture:
# x = x.unsqueeze(1)
# x = self.conv1d(x)
# x = x.view(x.size(0), -1)
# x = torch.sigmoid(self.fc1(x))
# x = torch.sigmoid(self.fc2(x))

# All shapes stated below are for a single input batch, that is, we ignore the batch dimension.

# Suppose input is [a, b, c, ..., z] (pretend there are 50 entries)
# Notice that all values in the input are INTEGERS

# After x.unsqueeze(1), we get:
# [[a, b, c, ..., z]], shape = (1, 50)

# conv1d.weight = torch.tensor([[[1., 1.]], [[2., 3.]]])
# conv1d.bias = torch.tensor([0., 0.])

# After self.conv1d(x), we get:
# [
#     [1a + 1b, 1b + 1c, ..., 1y + 1z],
#     [2a + 3b, 2b + 3c, ..., 2y + 3z]
# ], shape = (2, 49)

# After x.view(x.size(0), -1), we flatten the output to:
# [1a + 1b, 1b + 1c, ..., 1y + 1z, 2a + 3b, 2b + 3c, ..., 2y + 3z]

# %%
# 'fc1.weight': tensor([[ 100.,    0.,    0.,  ...,    0.,    0.,    0.],
# [-100.,    0.,    0.,  ...,    0.,    0.,    0.],
# [   0.,  100.,    0.,  ...,    0.,    0.,    0.],
# ...,
# [   0.,    0.,    0.,  ...,    0., -100.,    0.],
# [   0.,    0.,    0.,  ...,    0.,    0.,  100.],
# [   0.,    0.,    0.,  ...,    0.,    0., -100.]]), 
# 'fc1.bias': tensor([
# -2.0650e+04,  2.0750e+04, -2.1850e+04,  2.1950e+04, -2.1450e+04,
# 2.1550e+04, -1.9850e+04,  1.9950e+04, -2.0250e+04,  2.0350e+04,
# -2.1850e+04,  2.1950e+04, -2.1350e+04,  2.1450e+04, -2.2250e+04,
# 2.2350e+04, -2.3150e+04,  2.3250e+04, -2.0550e+04,  2.0650e+04,
# -2.1750e+04,  2.1850e+04, -2.1850e+04,  2.1950e+04, -1.4850e+04,
# 1.4950e+04, -1.4550e+04,  1.4650e+04, -2.0450e+04,  2.0550e+04,
# -1.6050e+04,  1.6150e+04, -1.7050e+04,  1.7150e+04, -2.3550e+04,
# 2.3650e+04, -2.1050e+04,  2.1150e+04, -2.1050e+04,  2.1150e+04,
# -2.2050e+04,  2.2150e+04, -2.1350e+04,  2.1450e+04, -1.5950e+04,
# 1.6050e+04, -1.4550e+04,  1.4650e+04, -2.0850e+04,  2.0950e+04,
# -1.6450e+04,  1.6550e+04, -1.6850e+04,  1.6950e+04, -2.1850e+04,
# 2.1950e+04, -2.1450e+04,  2.1550e+04, -1.6650e+04,  1.6750e+04,
# -1.5350e+04,  1.5450e+04, -1.9550e+04,  1.9650e+04, -1.7050e+04,
# 1.7150e+04, -1.5150e+04,  1.5250e+04, -1.5250e+04,  1.5350e+04,
# -1.7150e+04,  1.7250e+04, -1.4350e+04,  1.4450e+04, -1.5850e+04,
# 1.5950e+04, -2.2450e+04,  2.2550e+04, -2.3050e+04,  2.3150e+04,
# -2.1650e+04,  2.1750e+04, -1.9750e+04,  1.9850e+04, -1.9650e+04,
# 1.9750e+04, -2.2450e+04,  2.2550e+04, -1.2450e+04,  1.2550e+04,
# 5.0000e+01,  5.0000e+01,  5.0000e+01,  5.0000e+01,  5.0000e+01,
# 5.0000e+01,  5.0000e+01,  5.0000e+01, -5.1850e+04,  5.1950e+04,
# -5.5150e+04,  5.5250e+04, -5.3050e+04,  5.3150e+04, -4.9550e+04,
# 4.9650e+04, -5.1050e+04,  5.1150e+04, -5.5150e+04,  5.5250e+04,
# -5.2750e+04,  5.2850e+04, -5.6850e+04,  5.6950e+04, -5.7250e+04,
# 5.7350e+04, -5.0850e+04,  5.0950e+04, -5.5650e+04,  5.5750e+04,
# -5.3550e+04,  5.3650e+04, -3.4850e+04,  3.4950e+04, -3.8650e+04,
# 3.8750e+04, -5.1950e+04,  5.2050e+04, -3.7250e+04,  3.7350e+04,
# -4.6150e+04,  4.6250e+04, -5.8750e+04,  5.8850e+04, -5.1650e+04,
# 5.1750e+04, -5.3750e+04,  5.3850e+04, -5.4650e+04,  5.4750e+04,
# -5.3650e+04,  5.3750e+04, -3.7050e+04,  3.7150e+04, -3.8650e+04,
# 3.8750e+04, -5.3150e+04,  5.3250e+04, -3.8050e+04,  3.8150e+04,
# -4.5550e+04,  4.5650e+04, -5.3850e+04,  5.3950e+04, -5.4350e+04,
# 5.4450e+04, -3.8650e+04,  3.8750e+04, -4.0850e+04,  4.0950e+04,
# -4.8650e+04,  4.8750e+04, -4.1750e+04,  4.1850e+04, -3.7950e+04,
# 3.8050e+04, -3.8250e+04,  3.8350e+04, -4.3850e+04,  4.3950e+04,
# -3.3650e+04,  3.3750e+04, -4.2750e+04,  4.2850e+04, -5.6450e+04,
# 5.6550e+04, -5.7750e+04,  5.7850e+04, -5.3450e+04,  5.3550e+04,
# -4.9250e+04,  4.9350e+04, -4.9350e+04,  4.9450e+04, -5.7450e+04,
# 5.7550e+04, -2.4950e+04,  2.5050e+04,  5.0000e+01,  5.0000e+01,
# 5.0000e+01,  5.0000e+01,  5.0000e+01,  5.0000e+01,  5.0000e+01,
# 5.0000e+01])

# Investigate the fc1 weights more closely:
for i in range(model_weights['fc1.weight'].shape[0]):
    for j in range(model_weights['fc1.weight'].shape[1]):
        if model_weights['fc1.weight'][i][j] != 0:
            print(f"fc1.weight[{i}][{j}] = {model_weights['fc1.weight'][i][j]}")

# input_to_fc1 = [1a + 1b, 1b + 1c, ..., 1y + 1z, 2a + 3b, 2b + 3c, ..., 2y + 3z]
# Notice that all of these values are still INTEGERS
# Simply speaking, fc1_output[i] = (-1)**i * 100 * input_to_fc1[i // 2] + bias[i]
# And the output of this layer is sigmoid(fc1_output)
# The outputs are 196 values, each of them are 0 to 1 floating point numbers.

# %%
# fc2.weight = torch.tensor([[100.] * 196])
# fc2.bias = torch.tensor([-19550.])

# x = torch.sigmoid(self.fc2(x)) technically means:
# sigmoid(input_to_fc2.sum() * 100 - 19550) # input_to_fc2 has shape (196,)

# And we want output.item() > 0.5:
# So we need:
# input_to_fc2.sum() * 100 - 19550 > 0
# input_to_fc2.sum() * 100 > 19550
# input_to_fc2.sum() > 195.5
# 196 0-1 floating point entries and should have a sum greater than 195.5

# %%
# Have a closer look at the fc1 biases, they are all large numbers.
# More specifically, bias % 100 == 50
# Consider the formula:
# sigmoid((-1)**i * 100 * input_to_fc1[i // 2] + bias[i])
# = sigmoid((Some integer) * 100 + 50)
# So the output of fc1 must be very close to 1 or 0, since the input to sigmoid is a large number (at least 50 in absolute value).
# We can simply use 1 or 0 to represent the output of fc1.

# %%
# We look at fc2 again,
# input_to_fc2.sum() > 195.5
# Given that the output of fc1 is either 0 or 1, we can simply count the number of 1s in the output of fc1.
# We can then reach a conclusion that all 196 outputs of fc1 must be 1s.
# That means, sigmoid((-1)**i * 100 * input_to_fc1[i // 2] + bias[i]) > 0.5
# So we need:
# (-1)**i * 100 * input_to_fc1[i // 2] + bias[i] > 0
# Or better yet, much greater than 0.

# %%
# We can then set some inequalities based on the above analysis:
# 100 * (1a + 1b) - 2.0650e+04 > 0
# -100 * (1a + 1b) + 2.0750e+04 > 0
# 100 * (1b + 1c) - 2.1850e+04 > 0
# -100 * (1b + 1c) + 2.1950e+04 > 0
# 100 * (1c + 1d) - 2.1450e+04 > 0
# etc.

# Rearranging the above inequalities, we get:
# (1a + 1b) > 206.5
# (1a + 1b) < 207.5
# (1b + 1c) > 218.5
# (1b + 1c) < 219.5
# (1c + 1d) > 214.5
# etc.

# Recall that the inputs are integers, we can then deduce that:
# 1a + 1b = 207
# 1b + 1c = 219
# 1c + 1d = 215
# etc.

# If you are good at observation, you will notice that the biases comes in pairs of (x, -x + 100),
# That means, the inequalities can be combined into exact equations

# These can be solved as a system of equations:
# You are given inequalities in terms of 1a+1b, 1b+1c, 1c+1d, etc, and also 2a+3b, 2b+3c, etc.
# A unique solution can be solved
# Alternatively, given the flag format, we can also easily solve for the flag.

# %%
bias = model_weights['fc1.bias']
part1 = (bias[1:bias.shape[0]//2:2] - 50) / 100
part2 = (bias[bias.shape[0]//2+1::2] - 50) / 100
print(part1)
print(part2)

# %%
# The equations are:
for i in range(49):
    print(f"x_{i} + x_{i+1} = {part1[i]}")
    print(f"2x_{i} + 3x_{i+1} = {part2[i]}")

# %%
# Solve the equations:
from sympy import symbols, Eq, solve
x = symbols('x0:50')
equations = []
for i in range(49):
    equations.append(Eq(x[i] + x[i + 1], part1[i]))
    equations.append(Eq(2 * x[i] + 3 * x[i + 1], part2[i]))
solution = solve(equations, x)

# %%
# Print the solution
for i in range(50):
    print(f"x_{i} = {int(solution[x[i]])}")

flag = ""
for i in range(50):
    flag += chr(int(solution[x[i]]))

print(f"flag = {flag}")