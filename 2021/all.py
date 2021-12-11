#!/usr/bin/env python3

# HELPER FUNCTIONS
import os
import re
import subprocess

if __name__ == '__main__':
    dir_ = os.path.dirname(os.path.abspath(__file__))
    sols = sorted([f for f in os.listdir(dir_) if re.match(r'^\d+\.py$', f)])
    with open(os.path.join(dir_, 'solutions.txt'), 'w') as out:
        for s in sols:
            mes = f"===Running {s}==="
            print(mes)
            out.write(mes + "\n")
            result = subprocess.run(['python', os.path.join(dir_, s)], stdout=subprocess.PIPE)
            mes = result.stdout.decode('utf-8')
            print(mes, end='')
            out.write(mes)
