#!/usr/bin/env python3


import os
import re
import subprocess
import sys


def call_out(command: str, **kwargs):
    """
    Call shell command and return its output
    :param command: shell command to execute, supports shell pipes
    :return: output of command
    """
    # print("$ " + command, file=sys.stderr, flush=True)
    ps = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **kwargs)
    output_ = ps.communicate()[0] or bytearray()
    return output_.decode(sys.stdout.encoding or 'utf-8').strip()


if __name__ == '__main__':
    dir_ = os.path.dirname(os.path.abspath(__file__))
    sols = sorted([f for f in os.listdir(dir_) if re.match(r'^\d+\.py$', f)])
    with open(os.path.join(dir_, 'answers.txt'), 'w') as out:
        for s in sols:
            mes = f"===Running {s}==="
            print(mes)
            out.write(mes + "\n")
            mes = call_out(f"python {os.path.join(dir_, s)}")
            print(mes)
            out.write(mes + '\n')
