#!/usr/bin/env python3
import sys

s = sys.argv[1].replace("_", " ")
print('\n'," ".join(s[i:i+2] for i in range(0, len(s), 2)))