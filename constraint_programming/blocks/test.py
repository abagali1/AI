#!/usr/bin/env python3
import blocks

blocks.PZL_HEIGHT = blocks.PZL_WIDTH = 5
blocks.INDICES = {index: (index // 5, (index % 5))
               for index in range(25)}
blocks.INDICES_2D = {(i, j): i * 5 + j for i in range(5)
                  for j in range(5)}
pzl = "AABBBAABBBAA............."
idx = 2*5 + 2
print(blocks.find_neighbor_values(pzl,idx))