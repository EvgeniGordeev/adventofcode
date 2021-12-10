#!/usr/bin/env python3

# HELPER FUNCTIONS
import os
import re

if __name__ == '__main__':
    dir_ = os.path.dirname(__file__)
    sols = sorted([f for f in os.listdir(dir_) if re.match(r'^\d+\.py$', f)])
    for s in sols:
        print(f"===Running {s}===")
        os.system(f"python {s}")
        # exec(open(os.path.join(dir_, s)).read())
