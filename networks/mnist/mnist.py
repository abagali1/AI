import sys
import torch
import torch.nn as nn

device = 'cpu'

zo = [0.0, 1.0]  # zo = zero-one
ins = torch.tensor([[a, b, c] for a in zo for b in zo for c in zo])
expected = torch.tensor([[sum(tpl) % 2] for tpl in ins])
nodeCts = [len(ins[0]), 2, 1]

print(ins, expected, nodeCts)

netSpec = [torch.nn.Sigmoid() if i % 2 else
           torch.nn.Linear(nodeCts[i // 2], nodeCts[1 + i // 2], bias=i < 1)
           for i in range(2 * len(nodeCts) - 2)]

mynn = torch.nn.Sequential(*netSpec, torch.nn.Linear(1, 1, bias=False))
criterion = torch.nn.MSELoss()

optimizer = torch.optim.SGD(mynn.parameters(), lr=0.5)
for epoch in range(40000 + 1):
    y_pred = mynn(ins)  # Forward propagation
    loss = criterion(y_pred, expected)  # Compute and print error
    if not epoch % 500 or epoch < 10:
        print('epoch: ', epoch, ' loss: ', loss.item())
    optimizer.zero_grad()  # Zero the gradients
    loss.backward()  # Back propagation
    optimizer.step()  # Update the weights

for k, v in mynn.state_dict().items():
    print(k, v)
