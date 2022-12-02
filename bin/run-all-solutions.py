#!/usr/bin/env python3
import argparse
import os
import re
import subprocess
import sys
import tempfile


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
    parser = argparse.ArgumentParser(description='Execute all py files in a folder and [write answers to a file]')
    parser.add_argument('--dir', default='../2022', help='folder with py files to run')
    parser.add_argument('--write', action='store_true', help='write results to answers.txt')
    args = parser.parse_args()

    folder = os.path.join(os.getcwd(), args.dir)
    if not os.path.isdir(folder):
        sys.exit(f" --dir requires an existing folder. {folder} is not a directory. ")

    sols = sorted([f for f in os.listdir(folder) if re.match(r'^\d+\.py$', f)])
    answers = os.path.join(folder, 'answers.txt') if args.write else tempfile.NamedTemporaryFile().name
    folder_name = folder.split('/')[-1]
    with open(answers, 'w', encoding='utf-8') as out:
        for s in sols:
            mes = f"{folder_name}/{s}"
            print(mes)
            out.write(mes + "\n")
            mes = call_out(f"python {os.path.join(folder, s)}")
            mes = "  " + mes.replace('\n', '\n  ')
            print(mes)
            out.write(mes + '\n')
