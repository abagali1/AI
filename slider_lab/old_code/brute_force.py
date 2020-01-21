import subprocess
from itertools import permutations

perms = permutations("12345678_")

for x in perms:
    process = subprocess.Popen(["python3", "/home/abagali1/Desktop/AI/SEM1/slider_lab/old_code/slider_quiz_2.py", f"{x}"], stdout=subprocess.PIPE)
    out, err = process.communicate()
    out = out.decode('utf-8')
    print(out)
    for x,y in zip([*x], [*out[1]]):
        if x == y:
            break
        print(out[1])
